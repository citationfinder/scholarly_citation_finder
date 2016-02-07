from django.http import HttpResponse
from scholarly_citation_finder.api.citation.strategy.AuthorStrategy import AuthorStrategy
from scholarly_citation_finder.api.citation.strategy.JournalStrategy import JournalStrategy
from scholarly_citation_finder.api.citation.strategy.ConferenceStrategy import ConferenceStrategy
from scholarly_citation_finder.api.citation.CitationFinder import CitationFinder
from scholarly_citation_finder.api.citation.strategy.FieldofstudyStrategy import FieldofstudyStrategy


def index(request):
    author_name = request.GET.get('author_name', None)
    author_id = request.GET.get('author_id', None)
    
    if author_name or author_id:
        citation_finder = CitationFinder()
        citation_finder.set_by_author(name=author_name, id=author_id)
        
        #citation_finder.run(AuthorStrategy())
        #citation_finder.run(AuthorStrategy(ordered=True))
        citation_finder.run(AuthorStrategy(ordered=True, recursive=True))
        #citation_finder.run(JournalStrategy())
        #citation_finder.run(JournalStrategy(ordered=True))
        #citation_finder.run(ConferenceStrategy())
        #citation_finder.run(ConferenceStrategy(ordered=True))
        #citation_finder.run(FieldofstudyStrategy())
        #citation_finder.run(FieldofstudyStrategy(ordered=True))
        return HttpResponse('Done')
    else:
        return HttpResponse('Nothing to do. Usage: ?author_name=<name> or ?author_id=<id>')