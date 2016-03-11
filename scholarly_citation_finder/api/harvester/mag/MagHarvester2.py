import os.path
import csv
import logging
from django.db.utils import IntegrityError

from scholarly_citation_finder.apps.core.models import FieldOfStudyHierarchy
from .MagNormalize import MagNormalize


logger = logging.getLogger(__name__)


class MagHarvester2:

    def __init__(self, path, database='mag'):
        self.path = path
        self.database = database
        
    def run(self, name, callback):
        if name not in MagNormalize.FILES:
            raise Exception('unknown name')
        
        filename = os.path.join(self.path, MagNormalize.FILES[name])
        with open(filename, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            reader.next()
            for row in reader:
                try:
                    callback(row)
                except(IntegrityError) as e:
                    logger.info('{}:{}'.format(type(e).__name__, str(e)))

    def field_of_study_hierarchy(self, row):
        FieldOfStudyHierarchy.objects.using(self.database).get_or_create(child_id=row[0],
                                                                         child_level=row[1],
                                                                         parent_id=row[2],
                                                                         parent_level=row[3],
                                                                         confidence=row[4])
