#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarly_citation_finder.settings.development')

application = get_wsgi_application()
