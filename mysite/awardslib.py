# coding: utf-8

import urllib
import hashlib
import datetime

try:
    import json
except ImportError:
    import simplejson as json

def h(s):
    return hashlib.sha1(s).hexdigest()

def sign_args(args, key):
    return hashlib.sha1(urlencode_sorted(args) + key).hexdigest()

def verify_sig(sig, args, key):
    return sig == sign_args(args, key)

def urlencode_sorted(args):
    return urllib.urlencode(sorted(args.items()))

class AwardClient:
    service_url = "http://whatisav.co.uk/api/"

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

def django_fingerprint(request):
    # Make a fingerprint from the django request object
    fingerprint = [("useragent-sha1", h(request.META['HTTP_USER_AGENT'])),]

    if 'HTTP_X_FORWARDED_FOR' in request.META:
        fingerprint.append(("ip-sha1", h(request.META['HTTP_X_FORWARDED_FOR'])))
    else:
        fingerprint.append(("ip-sha1", h(request.META['REMOTE_ADDR'])))

    if request.user.is_authenticated():
        fingerprint.append( ("email-sha1", h(request.user.email)) )
    return fingerprint

