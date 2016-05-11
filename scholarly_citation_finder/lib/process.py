import subprocess32 as subprocess

class ProcessException(Exception):
    pass


def external_process(process_args, input_data='', timeout=None, cwd=None):
    '''
    Function from:
    @see https://github.com/SeerLabs/extractor-framework/blob/master/extraction/utils.py
    
    Pipes input_data via stdin to the process specified by process_args and returns the results

    Arguments:
      process_args -- passed directly to subprocess.Popen(), see there for more details
      input_data -- the data to pipe in via STDIN (optional)
      timeout -- number of seconds to time out the process after (optional)
        IF the process timesout, a subprocess32.TimeoutExpired exception will be raised

    Returns:
      (exit_status, stdout, stderr) -- a tuple of the exit status code and strings containing stdout and stderr data

    Examples:
      >>> external_process(['grep', 'Data'], input_data="Some String\nWith Data")
      (0, 'With Data\n', '')
    '''
    process = subprocess.Popen(process_args,
                               stdout=subprocess.PIPE,
                               stdin=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               cwd=cwd)
    try:
        (stdout, stderr) = process.communicate(input_data, timeout)
    except (subprocess.TimeoutExpired) as e:
        # cleanup process
        # see https://docs.python.org/3.3/library/subprocess.html?highlight=subprocess#subprocess.Popen.communicate
        process.kill()
        process.communicate()
        raise ProcessException('{}: {}'.format(type(e).__name__), str(e))

    exit_status = process.returncode
    return (exit_status, stdout, stderr)


def external_process2(process_args, cwd=None):
    '''
    Open a subprocess.

    :param process_args: Process arguments
    :param cwd: Directory
    '''
    return subprocess.Popen(process_args,
                            stdout=None,
                            stdin=None,
                            stderr=None,
                            cwd=cwd)
