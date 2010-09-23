# coding: utf-8

import hashlib
import time

try:
    import json
except ImportError:
    import simplejson as json

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from awards.settings import SECRET_KEY

from models import RegisteredSite, Fingerprint, Award

from awardslib import AwardClient, django_fingerprint

award_client = AwardClient("awards", "0123456789")
this_source = RegisteredSite.objects.get(slug="awards")

def django_fingerprint_login(request, fingerprint):
    # Attempt to log a user in with their fingerprint or cookie
    user = None
    try:
        user = find_user(this_source, fingerprint)
    except Fingerprint.CannotMatch:
        pass

    if user is not None:
        user = authenticate(username=user.username, password='')
        login(request, user)

def decorator_fingerprint_login(f):
    def fn(request, *args, **kwargs):
        if not request.user.is_authenticated():
            fingerprint = django_fingerprint(request)
            django_fingerprint_login(request, fingerprint)
        return f(request, *args, **kwargs)
    return fn
    
def render_with_context(request,
                        template,
                        context,
                        **kw):
    kw['context_instance'] = RequestContext(request)
    return render_to_response(template,
                              context,
                              **kw)

@decorator_fingerprint_login
def home(request):
    context = {'awards': {},}

    awards = Award.objects.filter(user=request.user).order_by("source").all()
    for award in awards:
        if award.source in context['awards']:
            context['awards'][award.source].append(award)
        else:
            context['awards'][award.source] = [award]

    return render_with_context(request, "mysite/home.html", context)

def client(request):
    fingerprint = django_fingerprint(request)
    award_client.make_award("Visited the awards site", fingerprint)
    
    return HttpResponseRedirect("/")

def find_user(source, fingerprint):
    fingerprint_misses = []

    user = None
    
    for print_type, data in fingerprint:
        fingerprint = None
        try:
            fingerprint = Fingerprint.objects.get(print_type=print_type, data=data)
        except Fingerprint.DoesNotExist:
            pass

        if fingerprint is not None:
            if user is not None and fingerprint.user != user:
                raise Fingerprint.Contradiction() # This should prioritise different types, e.g. email > ip
            elif user is None:
                user = fingerprint.user
        else:
            fingerprint_misses.append((print_type, data))

    # If we identify the user, also add their other fingerprint info
    if user:
        for print_type, data in fingerprint_misses:
            Fingerprint.objects.create(user=user,
                                       print_type=print_type,
                                       data=data,
                                       source=source)

    if user is None:
        raise Fingerprint.CannotMatch()
    else:
        return user

def submit_award(request):
    POST = request.REQUEST
    COOKIES = request.COOKIES

    args = {}

    if 'source' in POST:
        try:
            source = RegisteredSite.objects.get(slug=POST['source'])
        except RegisteredSite.DoesNotExist:
            raise Http404("Can't find source: %s" % POST['source'])
    else:
        raise Http404("Please give a source slug")
    
    fingerprint = {}
    if 'fingerprint' in POST:
        fingerprint = json.loads(POST['fingerprint'])
    
    if 'awards_cookie' in COOKIES:
        fingerprint['cookie'] = COOKIES['awards_cookie']
    
    user = None
    temporary_user = False
    
    if request.user.is_authenticated():
        user = request.user
    else:
        try:
            user = find_user(source, fingerprint.items())
        except Fingerprint.CannotMatch:
            # Create a new temporary user
            random_username = "anon" + hashlib.sha1(str(time.time())).hexdigest()[:5]
            user = User.objects.create_user(random_username, random_username + "@awards")
            temporary_user = True 
        except Fingerprint.Contradiction:
            user = None

    award_name = POST['name']

    award_points = 0
    if 'points_value' in POST:
        award_points = int(POST['points_value'])

    award = None
    if user:
        award = Award.objects.make_award(award_name, user, source, award_points)

    response_text = ""

    if 'iframe' in POST and POST['iframe'] == "true":
        template_context = {'temporary_account': temporary_user,
                            'user': user,
                            'award_name': award_name,
                            'award_points': award_points,}
        response_text = render_to_string("mysite/iframe.html", template_context);
    else:    
        response_text = json.dumps({'temporary_account': temporary_user,
                                'user': str(user), })
    response = HttpResponse(response_text)
    
    # Find the cookie for this user, if not, make a new one
    cookie = None
    try:
        cookie = Fingerprint.objects.get(print_type="cookie",
                                         source=this_source,
                                         user=user)
    except Fingerprint.DoesNotExist:
        cookie_string = hashlib.sha1(user.username + user.email + SECRET_KEY).hexdigest()
        cookie = Fingerprint.objects.create(print_type="cookie",
                                            source=this_source,
                                            user=user,
                                            data=cookie_string)
        response.set_cookie('awards_cookie', value=cookie_string, max_age=86400*365)
    
    return response

    

