from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

class NoAuthBackend(ModelBackend):
    """
    Authenticates without requiring authorisation
    """
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

