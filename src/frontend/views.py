import string
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from core.models import Author, Citation, Publication, PublicationUrl
    
    
def authors_index(request):
    prefix = request.GET.get('prefix', 'A')
    return render(request, 'authors/index.html', {
        'authors': Author.objects.filter(last_name__startswith=prefix),
        'alphabet': list(string.ascii_uppercase)
    })


def authors_details(request, author_id):
    try:
        author = Author.objects.get(pk=author_id)
        context = {
            'author': author,
            'coauthors': author.coauthors.all(),
            'publications': author.publication_set.all(),
            'alphabet': list(string.ascii_uppercase)
        }
    except(ObjectDoesNotExist):
        context = {}

    return render(request, 'authors/details.html', context)


def publications_index(request):
    source = request.GET.get('source')
    if source == 'dblp':
        publications = Publication.objects.exclude(dblp_id=None)
    elif source == 'arxiv':
        publications = Publication.objects.exclude(arxiv_id=None)
    elif source == 'citeseerx':
        publications = Publication.objects.exclude(citeseerx_id=None)
    elif source == 'citeseerextractor':
        publications = Publication.objects.filter(extractor='citeseer_extractor')
    else:
        prefix = request.GET.get('prefix', 'A')
        publications = Publication.objects.filter(title__startswith=prefix)

    return render(request, 'publications/index.html', {
        'publications': publications,
        'source': source,
        'alphabet': list(string.ascii_uppercase)
    })


def publications_details(request, publication_id):
    try:
        publication = Publication.objects.get(pk=publication_id)
        context = {
            'publication': publication,
            'references': Citation.objects.filter(publication=publication),
            'citations': Citation.objects.filter(reference=publication),
            'urls': PublicationUrl.objects.filter(publication=publication),
            'alphabet': list(string.ascii_uppercase)
        }
    except(ObjectDoesNotExist):
        context = {}

    return render(request, 'publications/details.html', context)
