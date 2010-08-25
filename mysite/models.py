from django.db import models
from django.db.models import Model, Manager
from django.contrib.auth.models import User, UserManager

class RegisteredSite(Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80)
    url = models.URLField(verify_exists=False)
    description = models.TextField()
    secret_key = models.CharField(max_length=128) # Check actual length

    def __unicode__(self):
        return self.name

class Fingerprint(Model):
    user = models.ForeignKey(User)
    print_type = models.CharField(max_length=80)
    source = models.ForeignKey(RegisteredSite)
    data = models.TextField()

    def __unicode__(self):
        return "%s %s %s from %s" % (self.user, self.print_type, self.data, self.source)

    class CannotMatch(Exception):
        """
            Cannot match a user to this fingerprint
        """

    class Contradiction(Exception):
        """
            Conflicting fingerprints - more than one user matched
        """

class AwardManager(Manager):
    def make_award(self, name, user, source, points_value=0):
        # Does this user already have this award?
        award = None
        try:
            award = self.get(user=user, name=name, source=source)
        except Award.DoesNotExist:
            print "Doesn't exist"
        
        if award is not None:
            award.number += 1
            award.points_value += points_value
            award.save()
        else:
            award = self.create(user=user, name=name, source=source, number=1, points_value=points_value)

        return award

class Award(Model):
    name = models.CharField(max_length=80)
    user = models.ForeignKey(User)
    date_awarded = models.DateTimeField(auto_now_add=True)
    number = models.IntegerField(default=1)
    source = models.ForeignKey(RegisteredSite)
    points_value = models.IntegerField(default=0)
    
    objects = AwardManager()

    def __unicode__(self):
        return "%s for %s (%s) - %s from %s" % (self.name, self.user, self.date_awarded, self.number, self.source)

