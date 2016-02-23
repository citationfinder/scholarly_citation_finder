from __future__ import absolute_import
from celery import task

from .evaluation.Evaluation import Evaluation

@task
def create_evaluation(name, setsite, num_min_publications):
    e = Evaluation(name)
    e.create_random_author_set(setsite, num_min_publications)    
    return