from django.db import models

# Create your models here.
import os


class Patient(models.Model):
    name = models.CharField(max_length=255)
    id = models.CharField(max_length=100, primary_key=True)
    age = models.CharField(max_length=100)
    xml_file = models.FileField()

    def __unicode__(self):
        return self.id
