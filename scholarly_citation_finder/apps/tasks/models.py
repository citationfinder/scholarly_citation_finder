from django.db import models
from djcelery.models import TaskMeta

class Task(models.Model):
    TYPE_CITATION_MAG = 'citation/mag'
    
    TYPES = (
        (TYPE_CITATION_MAG, TYPE_CITATION_MAG),
    )
    
    type = models.CharField(max_length=30, choices=TYPES)
    starttime = models.DateTimeField(auto_now_add=True)
    taskmeta_id = models.CharField(max_length=100)