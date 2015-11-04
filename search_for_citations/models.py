from django.db import models

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.last_name

class Publication(models.Model):
    title =  models.CharField(max_length=150)
    abstract = models.TextField()
    journal = models.CharField(max_length=150)
    authors = models.ManyToManyField(Author)
    source = models.URLField()
    citeseerx_id = models.CharField(max_length=150)
    dblp_id = models.CharField(max_length=150)
    
    def __unicode__(self):
        return self.title
    
class Citation(models.Model):
    publication = models.OneToOneField(Publication, related_name='%(class)s_publication')
    citation = models.OneToOneField(Publication, related_name='%(class)s_citation')
    context = models.TextField()
    self = models.BooleanField()