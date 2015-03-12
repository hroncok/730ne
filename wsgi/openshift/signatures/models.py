from django.db import models
from django.contrib.auth import models as auth_models


class Signature(models.Model):
    user = models.OneToOneField(auth_models.User, primary_key=True)
    signed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
