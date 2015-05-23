from django.db import models
from jsonfield import JSONField

class Cluster(models.Model):
    name = models.CharField(max_length=128)
    
    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
        ordering = ('name',)

class Programme(models.Model):
    cluster = models.ForeignKey(Cluster)
    name = models.CharField(max_length=128)
    
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
    programme = models.ForeignKey(Programme)
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return u'%s: %s: %s' % (self.programme.cluster.name, self.programme.name, self.name)

    class Meta:
        ordering = ('name',)

class Revision(models.Model):
    project = models.ForeignKey(Project)
    edit = models.BooleanField(default=False)
    data = JSONField(null=True)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        ordering = ('updated_at',)
