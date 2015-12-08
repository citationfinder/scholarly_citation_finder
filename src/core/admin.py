from django.contrib import admin

from .models import Author, Publication, Citation

admin.site.register(Author)
admin.site.register(Publication)
admin.site.register(Citation)
