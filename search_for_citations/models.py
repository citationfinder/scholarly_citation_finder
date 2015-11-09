from django.db import models

class Author(models.Model):
    first_name = models.CharField(blank=True, null=True, max_length=100)
    last_name = models.CharField(blank=True, null=True, max_length=100)

    def __unicode__(self):
        return self.last_name

class Publication(models.Model):
    type = models.CharField(blank=True, null=True, max_length=150)
    title =  models.CharField(blank=True, null=True, max_length=150)
    authors = models.ManyToManyField(Author)
    date = models.CharField(blank=True, null=True, max_length=200)
    booktitle = models.CharField(blank=True, null=True, max_length=200)
    journal = models.CharField(blank=True, null=True, max_length=200)
    volume = models.CharField(blank=True, null=True, max_length=20)
    number = models.CharField(blank=True, null=True, max_length=20)    
    pages = models.CharField(blank=True, null=True, max_length=20)
    publisher = models.CharField(blank=True, null=True, max_length=150)
    abstract = models.TextField(blank=True, null=True)
    doi = models.CharField(blank=True, null=True, max_length=50)
    citeseerx_id = models.CharField(blank=True, null=True, max_length=150)
    dblp_id = models.CharField(blank=True, null=True, max_length=150)
    extractor = models.CharField(blank=True, null=True, max_length=150)    
    source = models.URLField(blank=True, null=True)
    source_extracted = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.title
    
class Citation(models.Model):
    publication = models.OneToOneField(Publication, related_name='%(class)s_publication')
    citation = models.OneToOneField(Publication, related_name='%(class)s_citation')
    context = models.TextField(blank=True, null=True)
    self = models.BooleanField(default=False)