import os.path
import csv
import logging
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from scholarly_citation_finder.apps.core.models import FieldOfStudyHierarchy,\
	PublicationKeyword, PublicationFieldOfStudy, FieldOfStudy
from .MagNormalize import MagNormalize, get_pre_name
from scholarly_citation_finder.lib.django import queryset_iterator
#from django.db import connections

logger = logging.getLogger(__name__)


class MagHarvester2:

	def __init__(self, path, database='mag'):
		self.path = path
		self.database = database
		
		#self.conn = connections[database]
		#self.cursor = self.conn.cursor()

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
				try:
					fieldofstudy = FieldOfStudy.objects.using(self.database).get(id=keyword.fieldofstudy_id)
					self.__store_fieldofstudy(keyword.publication_id, fieldofstudy_id=fieldofstudy.id, name=fieldofstudy.name, confidence=1)
				except(ObjectDoesNotExist) as e:
					logger.info(str(e))
					
	def __store_fieldofstudy(self, publication_id, fieldofstudy_id, name=None, level=10, confidence=1):
		try:
			PublicationFieldOfStudy.objects.using(self.database).create(publication_id=publication_id,
																		fieldofstudy_id=fieldofstudy_id,
																		fieldofstudy_name=name,
																		level=level,
																		confidence=confidence)
			return True
		except(IntegrityError) as e:
			logger.info(str(e))
		return False

	def __store_fieldofstudie_hierarchy(self, publication_id, fieldofstudy_id, recursive=False):
		result = []

		query = FieldOfStudyHierarchy.objects.using(self.database).filter(child_id=fieldofstudy_id)
		for hierarchy in query.iterator():
			result = True
			# store child (level 3 to 1)
			if hierarchy.child_id not in result:
				if self.__store_fieldofstudy(publication_id, fieldofstudy_id=hierarchy.child_id, name=hierarchy.child.name, level=hierarchy.child_level, confidence=1):
					result.append(hierarchy.child_id)

			# store parent (level 2 to 0)
			if hierarchy.parent_id not in result:
				if self.__store_fieldofstudy(publication_id, fieldofstudy_id=hierarchy.parent_id, name=hierarchy.parent.name, level=hierarchy.parent_level, confidence=hierarchy.confidence):
					result.append(hierarchy.parent_id)

			if recursive:
				self.__lop(publication_id, fieldofstudy_id=hierarchy.parent_id, recursive=recursive)

		return result
