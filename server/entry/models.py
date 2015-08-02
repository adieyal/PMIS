from django.db import models
from jsonfield import JSONField

class Cluster(models.Model):
    name = models.CharField(max_length=128)
    
    # def __unicode__(self):
        # return u'%s' % (self.name)

    def __unicode__(self):
        name = self.name
        upper = ''.join(filter(lambda c: c.isupper(), name))
        return upper

    class Meta:
        ordering = ('name',)

class Programme(models.Model):
    name = models.CharField(max_length=128)
    cluster = models.ForeignKey(Cluster)
    
    def __unicode__(self):
        return u'%s: %s' % (self.cluster.name, self.name)

    class Meta:
        ordering = ('name',)


class ImplementingAgent(models.Model):
    name = models.CharField(max_length=128)
    
    def __unicode__(self):
        return u'%s' % (self.name)
        
    class Meta:
        ordering = ('name',)

class Project(models.Model):
    cluster_id = models.CharField(max_length=64, null=True)
    project_id = models.CharField(max_length=64, null=True)
    revision_id = models.CharField(max_length=64, null=True)
    updated_at = models.DateTimeField(null=True)
    data = JSONField(null=True)
