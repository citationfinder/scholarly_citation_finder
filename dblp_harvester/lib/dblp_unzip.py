import gzip
import os.path
    
def unzip_file(filename):
    if os.path.isfile(filename):
        print('Unzip %s' % filename)
        inF = gzip.GzipFile(filename, 'rb')
        s = inF.read()
        inF.close()
    else:
        print('No file to unzip!')
        
unzip_file('dblp.xml.gz')