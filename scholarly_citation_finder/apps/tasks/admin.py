from django.contrib import admin
from djcelery.models import TaskMeta
from models import Task


class TaskMetaAdmin(admin.ModelAdmin):
    #readonly_fields = ('result',) <-- deactivated for debug
    pass

    
# Register 'default'
default_site = admin.site
default_site.register(TaskMeta, TaskMetaAdmin)
default_site.register(Task)