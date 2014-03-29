from django.db import models

class Cluster(models.Model):
    name = models.CharField(max_length=128)
    
    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
        ordering = ('name',)

class Programme(models.Model):
    name = models.CharField(max_length=128)
    cluster = models.ForeignKey('Cluster')
    
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
