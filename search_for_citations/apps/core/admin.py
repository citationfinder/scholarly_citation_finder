from django.contrib import admin

from .models import Author, Publication, PublicationReference, PublicationUrl


admin.site.register(Author)
admin.site.register(Publication)
admin.site.register(PublicationReference)
admin.site.register(PublicationUrl)
