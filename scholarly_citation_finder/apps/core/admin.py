from django.contrib import admin

from .models import Affilation, Author, Conference, ConferenceInstance, FieldOfStudy, Journal, Publication, PublicationAuthorAffilation, PublicationKeyword,PublicationReference, PublicationUrl

class MultiDBModelAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = ''

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(MultiDBModelAdmin, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_foreignkey(db_field, request=request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_manytomany(db_field, request=request, using=self.using, **kwargs)



'''
Register 'default'
'''
default_site = admin.site

default_site.register(Affilation)
default_site.register(Author)
default_site.register(Conference)
default_site.register(ConferenceInstance)
default_site.register(FieldOfStudy)
default_site.register(Journal)
default_site.register(Publication)
default_site.register(PublicationAuthorAffilation)
default_site.register(PublicationKeyword)
default_site.register(PublicationReference)
default_site.register(PublicationUrl)

from djcelery.models import TaskMeta
class TaskMetaAdmin(admin.ModelAdmin):
    readonly_fields = ('result',)    
default_site.register(TaskMeta, TaskMetaAdmin)


'''
Register 'mag'
'''
class MagAdminModel(MultiDBModelAdmin):
    using = 'mag'
    
mag_site = admin.AdminSite('mag')
mag_site.register(Affilation, MagAdminModel)
mag_site.register(Author, MagAdminModel)
mag_site.register(Conference, MagAdminModel)
mag_site.register(ConferenceInstance, MagAdminModel)
mag_site.register(FieldOfStudy, MagAdminModel)
mag_site.register(Journal, MagAdminModel)
mag_site.register(Publication, MagAdminModel)
mag_site.register(PublicationAuthorAffilation, MagAdminModel)
mag_site.register(PublicationKeyword, MagAdminModel)
mag_site.register(PublicationReference, MagAdminModel)
mag_site.register(PublicationUrl, MagAdminModel)

