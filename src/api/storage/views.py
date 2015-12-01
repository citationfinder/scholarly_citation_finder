from .Parser import Parser

def publications_index(request):
    return Parser.store_from_xml_file(request.GET.get('filelist', None) )