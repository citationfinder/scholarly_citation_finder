from django.db import models

class Author(models.Model):
    first_name = models.CharField(default=None, max_length=100)
    last_name = models.CharField(default=None, max_length=100)

    def __unicode__(self):
        return self.last_name

class Publication(models.Model):
    title =  models.CharField(default=None, max_length=150)
    authors = models.ManyToManyField(Author)
    date = models.DateField(default=None)
    booktitle = models.CharField(default=None, max_length=200)
    journal = models.CharField(default=None, max_length=200)
    volume = models.PositiveIntegerField(default=0)
    pages = models.CharField(default=None, max_length=20)
    publisher = models.CharField(default=None, max_length=150)
    abstract = models.TextField(default=None)
    doi = models.CharField(default=None, max_length=50)
    citeseerx_id = models.CharField(default=None, max_length=150)
    dblp_id = models.CharField(default=None, max_length=150)
    source = models.URLField(default=None)
    source_extracted = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.title
    
class Citation(models.Model):
    publication = models.OneToOneField(Publication, related_name='%(class)s_publication')
    citation = models.OneToOneField(Publication, related_name='%(class)s_citation')
    context = models.TextField()
    self = models.BooleanField(default=False)