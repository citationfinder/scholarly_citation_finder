import os.path
import csv
import logging
from django.db.utils import IntegrityError

from scholarly_citation_finder.apps.core.models import FieldOfStudyHierarchy,\
	PublicationKeyword, PublicationFieldOfStudy
from .MagNormalize import MagNormalize, get_pre_name
from scholarly_citation_finder.lib.django import queryset_iterator

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

	def publication_fieldofstudy(self):
		query = PublicationKeyword.objects.using(self.database).all()
		for keyword in queryset_iterator(query):
			self.__lop(fieldofstudy_id=keyword.fieldofstudy_id, publication_id=keyword.publication_id, store_child=True)

	def __lop(self, fieldofstudy_id, publication_id, store_child=False):
		query = FieldOfStudyHierarchy.objects.using(self.database).filter(child_id=fieldofstudy_id)
		for h in query.iterator():
			# store child (level 3 to 1)
			if store_child:
				try:
					PublicationFieldOfStudy.objects.using(self.database).create(publication_id=publication_id,
																				fieldofstudy_name=h.child.name,
																				level=h.child_level,
																				confidence=1)
				except(IntegrityError) as e:
					logger.info(str(e))
				store_child=False

			# store parent (level 2 to 0)
			try:
				PublicationFieldOfStudy.objects.using(self.database).create(publication_id=publication_id,
																			fieldofstudy_name=h.parent.name,
																			level=h.parent_level,
																			confidence=h.confidence)
			except(IntegrityError) as e:
				logger.info(str(e))
			self.__lop(fieldofstudy_id=h.parent_id, publication_id=publication_id)
