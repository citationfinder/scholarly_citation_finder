import os.path
from django.http import HttpResponse

import config
from .Parser import Parser


def publications_index(request):
    storage = Parser()

    param_filelist = request.GET.get('filelist', None)
    if param_filelist:
        file = os.path.join(config.DOWNLOAD_DIR, 'harvester', param_filelist)
        storage.store_from_xml_file(file)
        return HttpResponse('Finish')

    return HttpResponse('Nothing to do. Usage ?filelist=&lt;sample.xml&gt;')
