from django.contrib import admin

from .models import Author, Citation, Publication, PublicationUrl

admin.site.register(Author)
admin.site.register(Citation)
admin.site.register(PublicationUrl)
admin.site.register(Publication)
