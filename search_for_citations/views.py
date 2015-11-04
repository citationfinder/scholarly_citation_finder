from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .models import Author, Publication

def author_details(request, author_id):
    
    try:
        author = Author.objects.get(pk=author_id)
        context = {
            'author': author,
            'publications': author.publication_set.all()
        }
    except(ObjectDoesNotExist):
        context = {}
        
    return render(request, 'author/details.html', context)