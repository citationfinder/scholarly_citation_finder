import gzip
import os.path
import requests
from requests.exceptions import ConnectionError, InvalidSchema

from process import external_process, ProcessException


def create_dir(path):
    '''
    Creates the given path, if it does not already exists
    
    :param path: Directory path
    :return: Directory path
    '''
    if not os.path.exists(path):
        os.makedirs(path)
    return path
        

def download_file_process(url, cwd=None):
    '''
    Downloads a file by calling curl as external process

    :param url:
    :param cwd:
    :return: file name
    '''
    exit_status, _, stderr = external_process(process_args=['curl', '-O', url],
                                              cwd=cwd)
    if exit_status != 0:
        raise ProcessException('Exit status is not 0, error: {}'.format(stderr))
    return url.rsplit('/', 1)[-1]


def extract_file_process(file, cwd):
    '''
    Extracts a file by calling 7-Zip as external process
    :param file:
    :param cwd:
    '''
    exit_status, _, stderr = external_process(process_args=['7z', 'x', file],
                                              cwd=cwd)
    if exit_status != 0:
        raise ProcessException('Exit status is not 0, error: {}'.format(stderr))
    return True


def download_file(url, path=None, name=None, expected_content_type=None):
    '''
    Downloads a single file. Can handle large files.
    '''
    if name:
        local_filename = os.path.join(path, name)
    else:
        local_filename = os.path.join(path, url.split('/')[-1])
    try:
        # NOTE the stream=True parameter
        r = requests.get(url, stream=True)
        r_content_type = r.headers['content-type']
        if expected_content_type and expected_content_type is not r_content_type:
            raise Exception('expected content-type {}, but was {}'.format(expected_content_type, r_content_type))
        with open(local_filename, 'wb') as f:
            #total_length = int(r.headers.get('content-length'))
            #for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    #f.flush() commented by recommendation from J.F.Sebastian
        return local_filename
    except(ConnectionError, InvalidSchema) as e:
        raise e


def unzip_file(filename, huge_file=True):
    if os.path.isfile(filename):
        outfilename = filename[:-3]
        input = gzip.open(filename, 'rb')
        output = open(outfilename, 'wb')
        if huge_file:
            while True:
                line = input.readline()
                if not line:
                    break
                output.write(line)
        else:          
            output.write(input.read())
        input.close()
        output.close()
        return outfilename
    else:
        raise Exception('{} is not a file (to unzip)'.format(filename))
