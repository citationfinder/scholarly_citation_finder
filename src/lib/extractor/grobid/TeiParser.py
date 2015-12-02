from lxml import etree

from lib.Parser import Parser

class TeiParser(Parser):
    
    def __init__(self):
        super(TeiParser, self).__init__('tei')
    
    def parse(self, xml):
        context = etree.iterparse(xml, html=True)
        self.fast_iter(context)
      
    def fast_iter(self, context):
        title = ''
        date = ''
        booktitle = ''
        journal = ''
        volume = ''
        number = ''
        pages = ''
        publisher = ''
        #abstract = ''
        author_array = []
        
        tmp_author_name = ''
        
        for _, elem in context:     
            #print("{}".format(elem.tag))
            if elem.tag == 'forename':
                tmp_author_name += elem.text+' '
            elif elem.tag == 'surname':
                tmp_author_name = elem.text + ', ' + tmp_author_name
            elif elem.tag == 'author':
                print(tmp_author_name)
                author_array.append(tmp_author_name)
                tmp_author_name = ''
            elif elem.tag == 'title' and 'level' in elem.attrib:
                # @see http://www.tei-c.org/release/doc/tei-p5-doc/de/html/ref-title.html
                if elem.attrib['level'] == 'a':
                    title = elem.text
                elif elem.attrib['level'] == 'j':
                    journal = elem.text
                elif elem.attrib['level'] == 'b':
                    booktitle = elem.text
            elif elem.tag == 'biblscope' and 'unit' in elem.attrib:
                if elem.attrib['unit'] == 'volume':
                    volume = elem.text
                elif elem.attrib['unit'] == 'issue':
                    number = elem.text
                elif elem.attrib['unit'] == 'page':
                    pages = '{}--{}'.format(elem.attrib.get('from'), elem.attrib.get('to'))
            elif elem.tag == 'date':
                if elem.attrib['type'] == 'published':
                    date = elem.attrib['when']
            elif elem.tag == 'publisher':
                publisher = elem.text
                    
            elif elem.tag == 'biblstruct':
                self.parse_citation(
                    context = elem.attrib.get('xml:id'),
                    title=title,
                    date=date,
                    booktitle=booktitle,
                    journal=journal,
                    number=number,
                    volume=volume,
                    pages=pages,
                    publisher=publisher,
                    extractor=self.name,
                    
                    authors=author_array,             
                )
                
                del author_array[:]
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
        del context                           