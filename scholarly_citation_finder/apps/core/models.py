from django.db import models


class Affilation(models.Model):
    name = models.CharField(max_length=150)

    def __unicode__(self):
        return unicode(self.name)


class Author(models.Model):
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return unicode(self.name)


class AuthorNameBlock(models.Model):
    name = models.CharField(db_index=True, max_length=52)
    
    def __unicode__(self):
        return unicode(self.name)


class AuthorNameVariation(models.Model):
    block = models.ForeignKey(AuthorNameBlock)
    author = models.ForeignKey(Author)
    first = models.CharField(max_length=20)
    middle = models.CharField(max_length=20, blank=True, null=True)
    last = models.CharField(max_length=50)
    suffix = models.CharField(max_length=10, blank=True, null=True)
    nickname = models.CharField(max_length=20, blank=True, null=True)
    
    def __unicode__(self):
        return unicode('{} {}'.format(self.first, self.last))


class Conference(models.Model):
    short_name = models.CharField(db_index=True, max_length=20, blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    
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


class FieldOfStudyHierarchy(models.Model):
    child = models.ForeignKey(FieldOfStudy, related_name='%(class)s_child')
    child_level = models.SmallIntegerField()
    parent = models.ForeignKey(FieldOfStudy, related_name='%(class)s_parent')
    parent_level = models.SmallIntegerField()
    confidence = models.FloatField()


class Journal(models.Model):
    name = models.CharField(db_index=True, max_length=250)
    
    def __unicode__(self):
        return unicode(self.name)


class KeywordFieldofstudy(models.Model):
    name = models.CharField(max_length=100)
    fieldofstudy = models.ForeignKey(FieldOfStudy, blank=True, null=True)
    #fieldofstudy_name = models.CharField(max_length=100, blank=True, null=True)
    #level = models.SmallIntegerField(blank=True, null=True)
    #confidence = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.name)    

    class Meta:
        unique_together = ('name', 'fieldofstudy')

class Publication(models.Model):
    """
    attributes
    """
    type = models.CharField(blank=True, null=True, max_length=50)
    title = models.CharField(db_index=True, blank=True, null=True, max_length=250)
    year = models.IntegerField(blank=True, null=True)
    date = models.CharField(blank=True, null=True, max_length=50)
    booktitle = models.CharField(blank=True, null=True, max_length=200)
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
    references
    """
    journal = models.ForeignKey(Journal, blank=True, null=True)
    conference = models.ForeignKey(Conference, blank=True, null=True)
    """
    other
    """
    source = models.CharField(blank=True, null=True, max_length=100)
    source_extracted = models.NullBooleanField(default=False)

    def __unicode__(self):
        return unicode(self.title)


class PublicationFieldOfStudy(models.Model):
    publication = models.ForeignKey(Publication)
    fieldofstudy = models.ForeignKey(FieldOfStudy, null=True)
    fieldofstudy_name = models.CharField(max_length=100)
    level = models.SmallIntegerField(blank=True, null=True)
    confidence = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = ('publication', 'fieldofstudy')

    def __unicode__(self):
        return unicode(self.fieldofstudy_name)


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
    extraction_date = models.DateTimeField(blank=True, null=True)
    
    def __unicode__(self):
        return unicode(self.url)


class PublicationReference(models.Model):
    publication = models.ForeignKey(Publication, related_name='%(class)s_publication')
    reference = models.ForeignKey(Publication, related_name='%(class)s_citation')
    context = models.TextField(blank=True, null=True)
    self = models.NullBooleanField(default=False)
    source = models.ForeignKey(PublicationUrl, blank=True, null=True)
