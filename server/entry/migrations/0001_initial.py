# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Project'
        db.create_table(u'entry_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cluster_id', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('redis_project_id', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'entry', ['Project'])

        # Adding model 'ProjectRevision'
        db.create_table(u'entry_projectrevision', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entry.Project'])),
            ('redis_revision_id', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('data', self.gf('jsonfield.fields.JSONField')()),
        ))
        db.send_create_signal(u'entry', ['ProjectRevision'])


    def backwards(self, orm):
        # Deleting model 'Project'
        db.delete_table(u'entry_project')

        # Deleting model 'ProjectRevision'
        db.delete_table(u'entry_projectrevision')


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
        u'entry.programme': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Programme'},
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entry.Cluster']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'entry.project': {
            'Meta': {'object_name': 'Project'},
            'cluster_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'redis_project_id': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'entry.projectrevision': {
            'Meta': {'object_name': 'ProjectRevision'},
            'data': ('jsonfield.fields.JSONField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entry.Project']"}),
            'redis_revision_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['entry']
