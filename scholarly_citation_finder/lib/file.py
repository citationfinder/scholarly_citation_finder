import os.path

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
        

def download_file(url, cwd=None):
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


def extract_file(file, cwd):
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