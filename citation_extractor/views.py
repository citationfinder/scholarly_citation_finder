from django.shortcuts import render

from django.http import HttpResponse
from search_for_citations.models import Publication
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import requests
from requests.exceptions import ConnectionError, InvalidSchema

def url_exits(url):
    #validate = URLValidator(verify_exists=True)
    try:
        validate = URLValidator()
        validate(url)
        response = requests.get(url)
        return response.status_code < 400
    except(ValidationError):
        return False
    except(ConnectionError, InvalidSchema):
        return False

def index(request):
    
    for publication in Publication.objects.filter(source__endswith='.pdf'):
        file_url = publication.source
        if url_exits(file_url):
            print(file_url)
        else:
            print("File does not exits: %s" % file_url)
    
    return HttpResponse("Hello, world. You're at the polls index.")