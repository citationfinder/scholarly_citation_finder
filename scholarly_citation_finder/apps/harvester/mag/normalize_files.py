import os
import codecs
import logging

#from scholarly_citation_finder import config

class MagNormalize():
	
	FILES = {
		'affiliations': 'Affiliations.txt',
		'authors': 'Authors.txt',
		'conferences': 'Conferences.txt',
		'conferences_instances': 'ConferenceInstances.txt',
		'fields_of_study': 'FieldsOfStudy.txt',
		'journals': 'Journals.txt',
		'papers': 'Papers.txt',
		'paper_author_affiliations': 'PaperAuthorAffiliations.txt',
		'paper_keywords': 'PaperKeywords.txt',
		'paper_references': 'PaperReferences.txt',
		'paper_urls': 'PaperUrls.txt'
	}
	
	def __init__(self, path):
		self.path = path
		self.logger = self.init_logger()
		
	def init_logger(self):
		logging.basicConfig(filename='{}.log'.format(self.__class__.__name__),
							level=logging.INFO,
							format='[%(asctime)s] %(levelname)s [%(module)s] %(message)s')
		return logging.getLogger()   	
		
	def run(self):
		self.logger.info('run -----------------------------')
		for name, file in self.FILES.iteritems():
			input = os.path.join(self.path, file)
			output = os.path.join(self.path, '{}_pre.txt'.format(file[:-4]))
			if os.path.isfile(input) and not os.path.isfile(output):
				try:
					output_file = codecs.open(output, 'w+')
					self.logger.info('start normalize {}'.format(input))
					getattr(self, name)(input, output_file)
					output_file.close
					self.logger.info('normalize done')
				except(Exception) as e:
					if output_file:
						output_file.close()
					if os.path.isfile(output):
						os.remove(output)
					self.logger.warn('{}: {}'.format(type(e).__name__, str(e)))
			else:
				self.logger.info('skip {}'.format(input))
		self.logger.info('run done ------------------------')

	def affiliations(self, input, output):
		'''
		Affiliations
		0	Affiliation ID
		1	Affiliation name
		
		:param input:
		:param output:
		'''
		with codecs.open(input) as f:
			output.write('ID\tName')
			for line in f:
				v = line.split('\t')
				if len(v[1]) <= 150:
					output.write('\n%s\t%s' % (int(v[0], 16), v[1].rstrip()))

	def authors(self, input, output):
		'''
		Authors
		0	Author ID
		1	Author name
	
		:param num_max_lines:
		'''
		with codecs.open(input) as f:
			output.write('ID\tName')
			for line in f:
				v = line.split('\t')
				if len(v[1]) <= 100:
					output.write('\n%s\t%s' % (int(v[0], 16), v[1].rstrip()))

	def conferences(self, input, output):
		'''
		ConferenceSeries
		0	Conference series ID
		1	Short name (abbreviation)
		2	Full name
		'''
		with codecs.open(input) as f:
			output.write('ID\tShort name\tName')
			for line in f:
				v = line.split('\t')
				if len(v[1]) <= 20 and len(v[2]) <= 250:
					output.write('\n%s\t%s\t%s' % (int(v[0], 16), v[1], v[2].rstrip()))
	
	def conferences_instances(self, input, output):
		'''
		0	Conference series ID
		1	Conference instance ID
		2	Short name (abbreviation)
		3	Full name
		4	Location
		5	Official conference URL
		6	Conference start date
		7	Conference end date
		8	Conference abstract registration date
		9	Conference submission deadline date
		10	Conference notification due date
		11	Conference final version due date
		'''
		with codecs.open(input) as f:
			output.write('ID\tConference ID\tShort name\tName\tLocation\tUrl\tYear')
			for line in f:
				v = line.split('\t')
				if len(v[2]) <= 40 and len(v[3]) <= 250 and len(v[4]) <= 100 and len(v[5]) <= 100:
					# Conference series ID
					if v[0]:
						v[0] = int(v[0], 16)
					# Conference start date
					if len(v[6]) == 10: # 2014/06/01
						v[6] = v[6][0:3]
					else:
						v[6] = ''
					output.write('\n%s\t%s\t%s\t%s\t%s\t%s\t%s' % (int(v[1], 16), v[0], v[2], v[3], v[4], v[5], v[6]))
	
	def fields_of_study(self, input, output):
		'''
		FieldsOfStudy
		0	Field of study ID
		1	Field of study name
		'''
		with codecs.open(input) as f:
			output.write('ID\t\tName')
			for line in f:
				v = line.split('\t')
				if len(v[1]) <= 100:
					output.write('\n%s\t%s' % (int(v[0], 16), v[1].rstrip()))
		
	def journals(self, input, output):
		'''
		Journals
		0	Journal ID
		1	Journal name
		'''
		with codecs.open(input) as f:
			output.write('ID\t\tName')
			for line in f:
				v = line.split('\t')
				if len(v[1]) <= 250:
					output.write('\n%s\t%s' % (int(v[0], 16), v[1].rstrip()))

	def papers(self, input, output):
		'''
		Papers
		0	Paper ID
		1	Original paper title
		2	Normalized paper title
		3	Paper publish year
		4	Paper publish date 
		5	Paper Document Object Identifier (DOI)
		6	Original venue name
		7	Normalized venue name
		8	Journal ID mapped to venue name
		9	Conference series ID mapped to venue name
		10	Paper rank
		'''
		with codecs.open(input) as f:
			output.write('Paper ID\tTitle\tYear\tDate\tDOI\tOriginal venue name\tJournal ID\tConference ID')
			for line in f:
				v = line.split('\t')
				if len(v[2]) <= 250 and len(v[5]) <= 50 and len(v[6]) <= 200:
					if len(v[4]) > 50:
						v[4] = ''
					if v[8]:
						v[8] = int(v[8], 16)
					if v[9]:
						v[9] = int(v[9], 16)						
					output.write('\n%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (int(v[0], 16), v[2], v[3], v[4], v[5], v[6], v[8], v[9]))
				
	def paper_author_affiliations(self, input, output):
		'''
		PaperAuthorAffiliations
		0	Paper ID
		1	Author ID
		2	Affiliation ID 
		3	Original affiliation name
		4	Normalized affiliation name
		5	Author sequence number
		'''
		with codecs.open(input) as f:
			output.write('\tPaper ID\tAuthor ID\tAffiliation ID')
			for line in f:
				v = line.split('\t')
				if v[2]:
					v[2] = int(v[2], 16)
				output.write('\n%s\t%s\t%s' % (int(v[0], 16), int(v[1], 16), v[2]))
		
	def paper_keywords(self, input, output):
		'''
		0	Paper ID
		1	Keyword name
		2	Field of study ID mapped to keyword
		'''
		with codecs.open(input) as f:
			output.write('Paper ID\t\tName\tField of study ID')
			for line in f:
				v = line.split('\t')
				if len(v[1]) <= 100: # TODO: may check if v[2] exists?
					output.write('\n%s\t%s\t%s' % (int(v[0], 16), v[1], int(v[2], 16)))

	def paper_references(self, input, output):
		'''
		PaperReferences
		0	Paper ID
		1	Paper reference ID
		'''
		with codecs.open(input) as f:
			output.write('Paper ID\tReference ID')
			for line in f:
				v = line.split('\t')
				output.write('\n%s\t%s' % (int(v[0], 16), int(v[1], 16)))

	def paper_urls(self, input, output):
		'''
		PaperUrls
		0	Paper ID
		1	URL
		'''
		with codecs.open(input) as f:
			output.write('Paper ID\tURL')
			for line in f:
				v = line.split('\t')
				if len(v[1]) <= 200:
					output.write('\n%s\t%s' % (int(v[0], 16), v[1]))
				else:
					#print(v[1])
					pass


#if __name__ == '__main__':
#	a = MagNormalize('E:\_mag\data\Authors')
#	a.run()