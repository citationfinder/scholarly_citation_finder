from __future__ import absolute_import
from celery import shared_task

from .evaluation.Evaluation import Evaluation

@shared_task
def create_evaluation(name, setsite, num_min_publications):
    e = Evaluation(name)
    e.create_random_author_set(setsite, num_min_publications)    
    return