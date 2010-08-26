# coding: utf-8
import json
import urllib
import hashlib
import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from models import RegisteredSite, Fingerprint, Award

def h(s):
    return hashlib.sha1(s).hexdigest()

def home(request):
    fingerprint = [("email-sha1", h("tfgg2@cam.ac.uk")), ("ip-sha1", h(request.META['REMOTE_ADDR']))]
    
    award_client = AwardClient("awards", "0123456789")
    award_client.make_award("Visited the awards site", fingerprint)

    user = fingerprint_user("awards", fingerprint)

    context = {'user': user,}

    awards = Award.objects.order_by("source").all()
    context['awards'] = {}

    for award in awards:
        if award.source in context['awards']:
            context['awards'][award.source].append(award)
        else:
            context['awards'][award.source] = [award]

    return render_to_response("mysite/home.html", context)

def sign_args(args, key):
    return hashlib.sha1(urlencode_sorted(args) + key).hexdigest()

def verify_sig(sig, args, key):
    return sig == sign_args(args, key)

def urlencode_sorted(args):
    return urllib.urlencode(sorted(args.items()))

class AwardClient:
    service_url = "http://localhost/api/"

    def __init__(self, slug, key):
        self.slug = slug
        self.key = key
    
    def make_award(self, award_name, fingerprint):
        args = {'source': self.slug,
                'name': award_name,
                'fingerprint': json.dumps(fingerprint),
                'time': datetime.datetime.now().isoformat()}
        
        url = "%s%s?%s&sig=%s" % (self.service_url, "submit_award", urlencode_sorted(args), sign_args(args, self.key))
        
        try:
            resp = urllib.urlopen(url)
            cval = resp.headers, resp.read()
        except IOError:
            cval = None, None 
def fingerprint_user(source, fingerprint):
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

    try:
        source = RegisteredSite.objects.get(slug=POST['source'])
    except KeyError:
        raise Http404("Please give a source slug")
    except RegisteredSite.DoesNotExist:
        raise Http404("Can't find source: %s" % POST['source'])

    args = {}
    args['source'] = POST['source']
    args['fingerprint'] = POST['fingerprint']
    args['name'] = POST['name']
    args['time'] = POST['time']
    
    if 'points_value' in POST:
        args['points_value'] = POST['points_value']

    if verify_sig(POST['sig'], args, source.secret_key) == False:
        raise Http404("Bad signature")
        
    fingerprint = json.loads(POST['fingerprint'])
    
    user = None
    try:
        user = fingerprint_user(source, fingerprint)
    except Fingerprint.CannotMatch:
        # Create a new user
        print "Cannot match"
        user = None
    except Fingerprint.Contradiction:
        print "Contradiction"
        user = None

    name = POST['name']

    points_value = 0
    if 'points_value' in POST:
        points_value = int(POST['points_value'])

    award = None
    if user:
        award = Award.objects.make_award(name, user, source, points_value)

    return HttpResponse(str(user))

    

