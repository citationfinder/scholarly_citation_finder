from django.db import models

class Author(models.Model):
    first_name = models.CharField(null=True, max_length=100)
    last_name = models.CharField(null=True, max_length=100)

    def __unicode__(self):
        return self.last_name

class Publication(models.Model):
    title =  models.CharField(null=True, max_length=150)
    authors = models.ManyToManyField(Author)
    date = models.DateField(null=True)
    journal = models.CharField(null=True, max_length=150)
    volume = models.PositiveIntegerField(default=0)
    publisher = models.CharField(null=True, max_length=150)
    abstract = models.TextField(null=True)
    doi = models.CharField(null=True, max_length=50)
    citeseerx_id = models.CharField(null=True, max_length=150)
    dblp_id = models.CharField(null=True, max_length=150)
    source = models.URLField(null=True)
    source_extracted = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.title
    
class Citation(models.Model):
    publication = models.OneToOneField(Publication, related_name='%(class)s_publication')
    citation = models.OneToOneField(Publication, related_name='%(class)s_citation')
    context = models.TextField()
    self = models.BooleanField(default=False)