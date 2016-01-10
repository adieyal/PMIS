# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Municipality'
        db.create_table(u'entry_municipality', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'entry', ['Municipality'])


    def backwards(self, orm):
        # Deleting model 'Municipality'
        db.delete_table(u'entry_municipality')


    models = {
        u'entry.cluster': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Cluster'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'entry.implementingagent': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ImplementingAgent'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'entry.municipality': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Municipality'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'entry.programme': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Programme'},
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entry.Cluster']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'entry.project': {
            'Meta': {'object_name': 'Project'},
            'cluster_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'data': ('jsonfield.fields.JSONField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'revision_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        }
    }

    complete_apps = ['entry']