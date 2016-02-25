from django.db import models
from djcelery.models import TaskMeta
from django.core.exceptions import ObjectDoesNotExist

class Task(models.Model):
    
    STATUS_SUCCESS = 'SUCCESS'
    STATUS_PENDING = 'PENDING'
    
    TYPE_CITATION_MAG = 'citation/mag'
    TYPE_EVALUATION_SET = 'evaluation/set'
    
    TYPES = (
        (TYPE_CITATION_MAG, TYPE_CITATION_MAG),
        (TYPE_EVALUATION_SET, TYPE_EVALUATION_SET)
    )
    
    type = models.CharField(max_length=30, choices=TYPES)
    starttime = models.DateTimeField(auto_now_add=True)
    taskmeta_id = models.CharField(max_length=100)

    def as_dict(self):
        return {'id': self.id,
                'starttime': self.starttime}
        
    def result(self):
        taskmeta = self.taskmeta()
        if taskmeta['status'] == self.STATUS_SUCCESS:
            return taskmeta['result'], taskmeta
        else:
            return False, taskmeta
        
    def taskmeta(self):
        try:   
            taskmeta = TaskMeta.objects.get(task_id=self.taskmeta_id)
            return {'id': self.id,
                    'starttime': self.starttime,
                    'date_done': taskmeta.date_done,
                    'result': str(taskmeta.result),
                    'status': taskmeta.status,
                    'traceback': taskmeta.traceback
                    }
        except(ObjectDoesNotExist):
            return {'id': self.id,
                    'starttime': self.starttime,
                    'status': ''}
    
    @staticmethod
    def get_tasks(type):
        items = []
        for task in Task.objects.filter(type=type):
            try:
                items.append(task.taskmeta())
            except(ObjectDoesNotExist):
                pass
        return items