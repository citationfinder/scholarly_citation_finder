from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from core.models import Author, Publication, Citation


def authors_index(request):
    return render(request, 'authors/index.html', {
        'authors': Author.objects.all()
    })


def authors_details(request, author_id):

    try:
        author = Author.objects.get(pk=author_id)
        context = {
            'author': author,
            'publications': author.publication_set.all()
        }
    except(ObjectDoesNotExist):
        context = {}

    return render(request, 'authors/details.html', context)


def publications_index(request, source):
    print(source)
    if source == 'dblp':
        publications = Publication.objects.exclude(dblp_id=None)
    if source == 'arxiv':
        publications = Publication.objects.exclude(arxiv_id=None)
    elif source == 'citeseerx':
        publications = Publication.objects.exclude(citeseerx_id=None)
    elif source == 'citeseerextractor':
        publications = Publication.objects.filter(extractor='citeseer_extractor')
    else:
        publications = Publication.objects.all()

    return render(request, 'publications/index.html', {
        'publications': publications,
        'source': source
    })


def publications_details(request, publication_id):
    try:
        publication = Publication.objects.get(pk=publication_id)
        context = {
            'publication': publication,
            'references': Citation.objects.filter(publication=publication),
            'citations': Citation.objects.filter(reference=publication)
        }
    except(ObjectDoesNotExist):
        context = {}

    return render(request, 'publications/details.html', context)
