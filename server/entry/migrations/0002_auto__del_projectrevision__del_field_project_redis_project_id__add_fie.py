# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ProjectRevision'
        db.delete_table(u'entry_projectrevision')

        # Deleting field 'Project.redis_project_id'
        db.delete_column(u'entry_project', 'redis_project_id')

        # Adding field 'Project.project_id'
        db.add_column(u'entry_project', 'project_id',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True),
                      keep_default=False)

        # Adding field 'Project.revision_id'
        db.add_column(u'entry_project', 'revision_id',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True),
                      keep_default=False)

        # Adding field 'Project.updated_at'
        db.add_column(u'entry_project', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'Project.data'
        db.add_column(u'entry_project', 'data',
                      self.gf('jsonfield.fields.JSONField')(null=True),
                      keep_default=False)


        # Changing field 'Project.cluster_id'
        db.alter_column(u'entry_project', 'cluster_id', self.gf('django.db.models.fields.CharField')(max_length=64, null=True))

    def backwards(self, orm):
        # Adding model 'ProjectRevision'
        db.create_table(u'entry_projectrevision', (
            ('redis_revision_id', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entry.Project'])),
            ('data', self.gf('jsonfield.fields.JSONField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'entry', ['ProjectRevision'])

        # Adding field 'Project.redis_project_id'
        db.add_column(u'entry_project', 'redis_project_id',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=64),
                      keep_default=False)

        # Deleting field 'Project.project_id'
        db.delete_column(u'entry_project', 'project_id')

        # Deleting field 'Project.revision_id'
        db.delete_column(u'entry_project', 'revision_id')

        # Deleting field 'Project.updated_at'
        db.delete_column(u'entry_project', 'updated_at')

        # Deleting field 'Project.data'
        db.delete_column(u'entry_project', 'data')


        # User chose to not deal with backwards NULL issues for 'Project.cluster_id'
        raise RuntimeError("Cannot reverse this migration. 'Project.cluster_id' and its values cannot be restored.")

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
            'cluster_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'data': ('jsonfield.fields.JSONField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'revision_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        }
    }

    complete_apps = ['entry']