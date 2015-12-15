import os.path
from django.http import HttpResponse

from search_for_citations import config
from .Parser import Parser
from ...core.models import Author, Publication


def publications_index(request):
    storage = Parser()

    param_filelist = request.GET.get('filelist', None)
    if param_filelist:
        file = os.path.join(config.DOWNLOAD_DIR, 'harvester', param_filelist)
        storage.store_from_xml_file(file)
        return HttpResponse('Finish')

    return HttpResponse('Nothing to do. Usage ?filelist=&lt;sample.xml&gt;')


def coauthors_index(request):
    authors = Author.objects.all()
    for author in authors:
        for author_publication in author.publication_set.all():
            for coauthor in author_publication.authors.exclude(last_name=author.last_name):
                author.coauthors.add(coauthor)
    return HttpResponse('Finish')