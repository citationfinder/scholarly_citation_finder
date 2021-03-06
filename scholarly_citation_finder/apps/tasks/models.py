from django.db import models
from djcelery.models import TaskMeta
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, viewsets


class Task(models.Model):
    
    STATUS_SUCCESS = 'SUCCESS'
    STATUS_PENDING = 'PENDING'
    
    TYPE_CITATION_FIND = 'citation/find'
    TYPE_CITATION_CRON = 'citation/cron'
    TYPE_CITATION_MAG = 'citation/mag'
    TYPE_EVALUATION_SET = 'evaluation/set'
    TYPE_EVALUATION_RUN = 'evaluation/run'
    TYPE_HARVESTER = 'harvester'
    
    type = models.CharField(max_length=30)
    starttime = models.DateTimeField(auto_now_add=True)
    taskmeta_id = models.CharField(max_length=100)

    def as_dict(self):
        return {'id': self.id,
                'starttime': self.starttime}
        
    def result(self, as_dict=True):
        taskmeta = self.get_taskmeta(as_dict=as_dict)
        if taskmeta['status'] == self.STATUS_SUCCESS and not taskmeta['traceback']:
            return taskmeta['result'], taskmeta
        else:
            return False, taskmeta
    
    def get_taskmeta(self, as_dict=False):
        if not hasattr(self, 'taskmeta'):
            try:   
                self.taskmeta = TaskMeta.objects.get(task_id=self.taskmeta_id)
            except(ObjectDoesNotExist):
                self.taskmeta = TaskMeta()
        if as_dict:
            return {'date_done': self.taskmeta.date_done,
                    'result': str(self.taskmeta.result),
                    'status': self.taskmeta.status,
                    'traceback': self.taskmeta.traceback}
        else:
            return self.taskmeta
    
class TaskSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.SerializerMethodField()
    date_done = serializers.SerializerMethodField()
    result = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    traceback = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        
    def get_date_done(self, obj):
        return obj.get_taskmeta().date_done
    
    def get_result(self, obj):
        return str(obj.get_taskmeta().result)
    
    def get_status(self, obj):
        return obj.get_taskmeta().status
    
    def get_traceback(self, obj):
        return obj.get_taskmeta().traceback

    def get_id(self, obj):
        return obj.id
    
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        queryset = Task.objects.all()
        type = self.request.query_params.get('type', None)
        if type:
            queryset = self.queryset.filter(type=type)
        return queryset
