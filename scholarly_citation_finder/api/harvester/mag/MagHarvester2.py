import csv
import logging

from scholarly_citation_finder.apps.core.models import FieldOfStudyHierarchy
from django.db.utils import IntegrityError

logger = logging.getLogger(__name__)


class MagHarvester2:

    def __init__(self, path):
        self.path = path
        
    def run(self, filename, callback):
        with open(filename, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            reader.next()
            for row in reader:
                try:
                    callback(row)
                except(IntegrityError) as e:
                    logger.info('{}:{}'.format(type(e).__name__, str(e)))

    def field_of_study_hierarchy(self, row):
        FieldOfStudyHierarchy.objects.get_or_create(child_id=row[0],
                                                    child_level=row[1],
                                                    parent_id=row[2],
                                                    parent_level=row[3],
                                                    confidence=row[4])
