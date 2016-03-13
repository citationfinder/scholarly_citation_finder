import os.path
import csv
import logging
from django.db.utils import IntegrityError

from scholarly_citation_finder.apps.core.models import FieldOfStudyHierarchy,\
	PublicationKeyword, PublicationFieldOfStudy
from .MagNormalize import MagNormalize, get_pre_name


logger = logging.getLogger(__name__)


class MagHarvester2:

	def __init__(self, path, database='mag'):
		self.path = path
		self.database = database

	def run(self, name, callback):
		if name not in MagNormalize.FILES:
			raise Exception('unknown name')

		filename = os.path.join(self.path, get_pre_name(MagNormalize.FILES[name]))
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

	def publication_fieldofstudy(self):
		for keyword in PublicationKeyword.objects.using(self.database).all():
			self.__lop(fieldofstudy_id=keyword.fieldofstudy_id, publication_id=keyword.publication_id, store_child=True)

	def __lop(self, fieldofstudy_id, publication_id, store_child=False):
		for h in FieldOfStudyHierarchy.objects.using(self.database).filter(child_id__in=fieldofstudy_id):
			# store child (level 3 to 1)
			if store_child:
				try:
					PublicationFieldOfStudy.objects.using(self.database).create(publication_id=publication_id,
																				fieldofstudy_name=h.child_name,
																				level=h.child_level,
																				confidence=1)
				except(Exception) as e:
					raise e
				store_child=False

			# store parent (level 2 to 0)
			PublicationFieldOfStudy.objects.using(self.database).create(publication_id=publication_id,
																		fieldofstudy_name=h.parent_name,
																		level=h.parent_level,
																		confidence=h.confidence)
			self.__lop(fieldofstudy_id=h.parent_id, publication_id=publication_id)
