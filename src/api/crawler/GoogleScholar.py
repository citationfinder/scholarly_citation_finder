#!/usr/bin/python
# -*- coding: utf-8 -*
import os.path
import logging
logger = logging.getLogger(__name__)

from core.process_manager.utils import external_process
from core.process_manager.Process import ProcessError

class GoogleScholar:
    
    SCHOLAR_PATH = os.path.join('lib', 'scholar.py', 'scholar.py')
    
    def get_pdf(self, title):
        
        try:
            status, stdout, stderr = external_process(['python', self.SCHOLAR_PATH, '--phrase', title, '-c 1', '--no-citations'])
            print(stderr)
            
            if status == 0:
                return stdout
            else:
                logger.warn('Unexpected return code {}, error may: {}'.format(status, stderr))
                return False
        except ProcessError as e:
            logger.warn(str(e))
        
        return False
