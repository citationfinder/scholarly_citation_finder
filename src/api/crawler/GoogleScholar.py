#!/usr/bin/python
# -*- coding: utf-8 -*
import os.path
import logging
logger = logging.getLogger(__name__)

from core.process_manager.utils import external_process
from core.process_manager.Process import ProcessError

class GoogleScholar:
    
    SCHOLAR_PATH = os.path.join('lib', 'scholar.py', 'scholar.py')
    
    def _parse_output(self, csv):   
        split = csv.split('|')
        if len(split) >= 7:
            url_pdf = split[6]
            if url_pdf is not ' ':
                logger.debug('found: {}'.format(url_pdf))
                return url_pdf
        return False
    
    def get_pdf(self, title):
        
        try:
            status, stdout, stderr = external_process(['python', self.SCHOLAR_PATH, '--phrase', title, '-c 1', '--no-citations', '--csv'])            
            if status == 0:
                return self._parse_output(stdout)
            else:
                logger.warn('Unexpected return code {}, error may: {}'.format(status, stderr))
                logger.warn('                           output is: {}'.format(stdout))
        except ProcessError as e:
            logger.warn(str(e))
        
        return False
