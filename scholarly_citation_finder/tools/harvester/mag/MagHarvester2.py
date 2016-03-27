import os.path
import csv
import logging
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from scholarly_citation_finder.apps.core.models import FieldOfStudyHierarchy,\
	PublicationKeyword, PublicationFieldOfStudy, FieldOfStudy
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
			result = self.__store_fieldofstudie_hierarchy(keyword.publication_id, fieldofstudy_id=keyword.fieldofstudy_id)
			if not result:
				self.__store_fieldofstudy(keyword.publication_id, fieldofstudy_id=keyword.fieldofstudy_id, confidence=1)
					
	def __store_fieldofstudy(self, publication_id, fieldofstudy_id=None, name=None, level=10, confidence=1):
		try:
			if not name:
				fieldofstudy = FieldOfStudy.objects.using(self.database).get(id=fieldofstudy_id)
				name = fieldofstudy.name
			PublicationFieldOfStudy.objects.using(self.database).create(publication_id=publication_id,
																		name=name,
																		level=level,
																		confidence=confidence)
		except(IntegrityError) as e:
			pass
		except(ObjectDoesNotExist) as e:
			logger.info(str(e))

	def __store_fieldofstudie_hierarchy(self, publication_id, fieldofstudy_id, store_child=True, recursive=False):
		result = False

		query = FieldOfStudyHierarchy.objects.using(self.database).filter(child_id=fieldofstudy_id)
		for hierarchy in query.iterator():
			result = True
			# store child (level 3 to 1)
			if store_child:
				self.__store_fieldofstudy(publication_id, name=hierarchy.child.name, level=hierarchy.child_level, confidence=1)
				store_child=False

			# store parent (level 2 to 0)
			self.__store_fieldofstudy(publication_id, name=hierarchy.parent.name, level=hierarchy.parent_level, confidence=hierarchy.confidence)				

			if recursive:
				self.__lop(publication_id, fieldofstudy_id=hierarchy.parent_id, store_child=False)

		return result
