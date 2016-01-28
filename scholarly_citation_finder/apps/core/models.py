from django.db import models


class Affilation(models.Model):
    name = models.CharField(max_length=150)

    def __unicode__(self):
        return unicode(self.name)


class Author(models.Model):
    name = models.CharField(max_length=100)
    #coauthors = models.ManyToManyField('self')
    
    def __unicode__(self):
        return unicode(self.name)


class Conference(models.Model):
    short_name = models.CharField(max_length=20)
    name = models.CharField(max_length=250)
    
    def __unicode__(self):
        return unicode(self.short_name)
    

class ConferenceInstance(models.Model):
    conference = models.ForeignKey(Conference, blank=True, null=True)
    short_name = models.CharField(max_length=40)
    name = models.CharField(max_length=250)
    location = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(max_length=100, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return unicode(self.short_name)

    
class FieldOfStudy(models.Model):
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return unicode(self.name)
    
    
class Journal(models.Model):
    name = models.CharField(max_length=250)
    
    def __unicode__(self):
        return unicode(self.name)

class Publication(models.Model):
    """
    attributes
    """
    type = models.CharField(blank=True, null=True, max_length=50)
    title = models.CharField(blank=True, null=True, max_length=250)
    year = models.IntegerField(blank=True, null=True)
    date = models.CharField(blank=True, null=True, max_length=50)
    booktitle = models.CharField(blank=True, null=True, max_length=200)
    journal = models.ForeignKey(Journal, blank=True, null=True)
    volume = models.CharField(blank=True, null=True, max_length=20)
    number = models.CharField(blank=True, null=True, max_length=20)
    pages_from = models.CharField(blank=True, null=True, max_length=5)
    pages_to = models.CharField(blank=True, null=True, max_length=5)
    series = models.CharField(blank=True, null=True, max_length=200)
    # edition
    # note
    # location
    publisher = models.CharField(blank=True, null=True, max_length=150)
    # institution
    # school
    # address
    isbn = models.CharField(blank=True, null=True, max_length=50)
    doi = models.CharField(blank=True, null=True, max_length=50)
    abstract = models.TextField(blank=True, null=True)
    copyright = models.TextField(blank=True, null=True)
    """
    other
    """
    source = models.CharField(blank=True, null=True, max_length=100)
    source_extracted = models.NullBooleanField(default=False)
    """
    mag only
    """
    conference = models.ForeignKey(Conference, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.title)


class PublicationAuthorAffilation(models.Model):
    publication = models.ForeignKey(Publication)
    author = models.ForeignKey(Author)
    affilation = models.ForeignKey(Affilation, blank=True, null=True)
    
    
class PublicationKeyword(models.Model):
    publication = models.ForeignKey(Publication)
    name = models.CharField(max_length=100)
    fieldofstudy = models.ForeignKey(FieldOfStudy, blank=True, null=True)
    
    def __unicode__(self):
        return unicode(self.name)
    

class PublicationReference(models.Model):
    publication = models.ForeignKey(Publication, related_name='%(class)s_publication')
    reference = models.ForeignKey(Publication, related_name='%(class)s_citation')
    context = models.TextField(blank=True, null=True)
    self = models.NullBooleanField(default=False)


class PublicationUrl(models.Model):
    MIME_TYPE_PDF = 'application/pdf'
    MIME_TYPE_HTML = 'text/html'
    MIME_TYPES = (
        ('', ''),
        (MIME_TYPE_PDF, 'PDF'),
        (MIME_TYPE_HTML, 'HTML'),
    )

    publication = models.ForeignKey(Publication)
    url = models.URLField(max_length=200)
    type = models.CharField(max_length=30, default='', choices=MIME_TYPES, blank=True, null=True)
    
    def __unicode__(self):
        return unicode(self.url)
