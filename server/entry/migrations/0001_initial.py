# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cluster'
        db.create_table(u'entry_cluster', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'entry', ['Cluster'])

        # Adding model 'Programme'
        db.create_table(u'entry_programme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cluster', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entry.Cluster'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'entry', ['Programme'])

        # Adding model 'ImplementingAgent'
        db.create_table(u'entry_implementingagent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'entry', ['ImplementingAgent'])

        # Adding model 'Project'
        db.create_table(u'entry_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('programme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entry.Programme'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'entry', ['Project'])

        # Adding model 'Revision'
        db.create_table(u'entry_revision', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entry.Project'])),
            ('edit', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('data', self.gf('jsonfield.fields.JSONField')(null=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal(u'entry', ['Revision'])


    def backwards(self, orm):
        # Deleting model 'Cluster'
        db.delete_table(u'entry_cluster')

        # Deleting model 'Programme'
        db.delete_table(u'entry_programme')

        # Deleting model 'ImplementingAgent'
        db.delete_table(u'entry_implementingagent')

        # Deleting model 'Project'
        db.delete_table(u'entry_project')

        # Deleting model 'Revision'
        db.delete_table(u'entry_revision')


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
            'Meta': {'ordering': "('name',)", 'object_name': 'Project'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'programme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entry.Programme']"})
        },
        u'entry.revision': {
            'Meta': {'ordering': "('updated_at',)", 'object_name': 'Revision'},
            'data': ('jsonfield.fields.JSONField', [], {'null': 'True'}),
            'edit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entry.Project']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        }
    }

    complete_apps = ['entry']