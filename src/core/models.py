from django.db import models

class Author(models.Model):
    first_name = models.CharField(blank=True, null=True, max_length=100)
    last_name = models.CharField(blank=True, null=True, max_length=100)

    def __unicode__(self):
        return unicode(self.last_name)

class Publication(models.Model):
    type = models.CharField(blank=True, null=True, max_length=150)
    title =  models.CharField(blank=True, null=True, max_length=150)
    authors = models.ManyToManyField(Author)
    date = models.CharField(blank=True, null=True, max_length=200)
    booktitle = models.CharField(blank=True, null=True, max_length=200)
    journal = models.CharField(blank=True, null=True, max_length=200)
    volume = models.CharField(blank=True, null=True, max_length=20)
    number = models.CharField(blank=True, null=True, max_length=20)    
    pages_from = models.CharField(blank=True, null=True, max_length=20)
    pages_to = models.CharField(blank=True, null=True, max_length=20)
    series = models.CharField(blank=True, null=True, max_length=150)
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
    copyright = models.CharField(blank=True, null=True, max_length=300)
    
    citeseerx_id = models.CharField(blank=True, null=True, max_length=150)
    dblp_id = models.CharField(blank=True, null=True, max_length=150)
    arxiv_id = models.CharField(blank=True, null=True, max_length=150)
    extractor = models.CharField(blank=True, null=True, max_length=150)    
    source_extracted = models.BooleanField(default=False)
    
    def __unicode__(self):
        return unicode(self.title)

class PublicationUrls(models.Model):
    MIME_TYPE_PDF = 'application/pdf'
    MIME_TYPES = (
        (MIME_TYPE_PDF, 'PDF'),
        ('text/html', 'HTML')
    )
    publication = models.ForeignKey(Publication)
    type = models.CharField(max_length=50, default=MIME_TYPE_PDF, choices=MIME_TYPES)
    url = models.URLField()
    
class Citation(models.Model):
    publication = models.ForeignKey(Publication, related_name='%(class)s_publication')
    reference = models.ForeignKey(Publication, related_name='%(class)s_citation')
    #publication = models.OneToOneField(Publication, related_name='%(class)s_publication')
    #reference = models.OneToOneField(Publication, related_name='%(class)s_citation')
    context = models.TextField(blank=True, null=True)
    self = models.BooleanField(default=False)