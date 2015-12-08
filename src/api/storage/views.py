from django.http import HttpResponse

from .Parser import Parser

def publications_index(request):
    storage = Parser()
    
    param_filelist = request.GET.get('filelist', None)
    if param_filelist:
        storage.store_from_xml_file(param_filelist)
        return HttpResponse('Finish')
    
    return HttpResponse('Nothing to do. Usage ?filelist=&lt;sample.xml&gt;') 
        