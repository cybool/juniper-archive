from django.db import models
from django.conf import settings


class Devices(models.Model):
    ### #######################################################
    ### Create db table to hold all of the Devices
    ### #######################################################
    hostname = models.CharField(max_length=255)
    compliant = models.BooleanField()
    diff = models.TextField(blank=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.hostname
