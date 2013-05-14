# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Client'
        db.create_table(u'pmis_client', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'pmis', ['Client'])

        # Adding model 'Municipality'
        db.create_table(u'pmis_municipality', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'pmis', ['Municipality'])

        # Adding model 'District'
        db.create_table(u'pmis_district', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('municipality', self.gf('django.db.models.fields.related.ForeignKey')(related_name='districts', to=orm['pmis.Municipality'])),
        ))
        db.send_create_signal(u'pmis', ['District'])

        # Adding model 'Programme'
        db.create_table(u'pmis_programme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(related_name='programmes', to=orm['pmis.Client'])),
        ))
        db.send_create_signal(u'pmis', ['Programme'])

        # Adding model 'Project'
        db.create_table(u'pmis_project', (
            ('cid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, db_index=True)),
            ('vid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 14, 0, 0))),
            ('update_comment', self.gf('django.db.models.fields.TextField')()),
            ('update_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('programme', self.gf('django.db.models.fields.related.ForeignKey')(related_name='projects', null=True, to=orm['pmis.Programme'])),
            ('municipality', self.gf('django.db.models.fields.related.ForeignKey')(related_name='projects', to=orm['pmis.Municipality'])),
        ))
        db.send_create_signal(u'pmis', ['Project'])

        # Adding M2M table for field district on 'Project'
        db.create_table(u'pmis_project_district', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'pmis.project'], null=False)),
            ('district', models.ForeignKey(orm[u'pmis.district'], null=False))
        ))
        db.create_unique(u'pmis_project_district', ['project_id', 'district_id'])

        # Adding model 'PeopleType'
        db.create_table(u'pmis_peopletype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'pmis', ['PeopleType'])

        # Adding model 'ProjectPeople'
        db.create_table(u'pmis_projectpeople', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='project_peoples', to=orm['pmis.Project'])),
        ))
        db.send_create_signal(u'pmis', ['ProjectPeople'])

        # Adding M2M table for field people_type on 'ProjectPeople'
        db.create_table(u'pmis_projectpeople_people_type', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('projectpeople', models.ForeignKey(orm[u'pmis.projectpeople'], null=False)),
            ('peopletype', models.ForeignKey(orm[u'pmis.peopletype'], null=False))
        ))
        db.create_unique(u'pmis_projectpeople_people_type', ['projectpeople_id', 'peopletype_id'])

        # Adding model 'ProjectFinancial'
        db.create_table(u'pmis_projectfinancial', (
            ('cid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, db_index=True)),
            ('vid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 14, 0, 0))),
            ('update_comment', self.gf('django.db.models.fields.TextField')()),
            ('update_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('total_anticipated_cost', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2)),
            ('project_planning_budget', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2)),
            ('project', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['pmis.Project'], unique=True)),
        ))
        db.send_create_signal(u'pmis', ['ProjectFinancial'])

        # Adding model 'Budget'
        db.create_table(u'pmis_budget', (
            ('cid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, db_index=True)),
            ('vid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 14, 0, 0))),
            ('update_comment', self.gf('django.db.models.fields.TextField')()),
            ('update_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('year', self.gf('django.db.models.fields.DateField')()),
            ('allocated_budget', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2)),
            ('project_financial', self.gf('django.db.models.fields.related.ForeignKey')(related_name='budgets', to=orm['pmis.ProjectFinancial'])),
        ))
        db.send_create_signal(u'pmis', ['Budget'])

        # Adding model 'ScopeCode'
        db.create_table(u'pmis_scopecode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'pmis', ['ScopeCode'])

        # Adding model 'ScopeOfWork'
        db.create_table(u'pmis_scopeofwork', (
            ('cid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, db_index=True)),
            ('vid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 14, 0, 0))),
            ('update_comment', self.gf('django.db.models.fields.TextField')()),
            ('update_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('scope_code', self.gf('django.db.models.fields.related.ForeignKey')(related_name='scope_of_works', to=orm['pmis.ScopeCode'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='scope_of_works', to=orm['pmis.Project'])),
        ))
        db.send_create_signal(u'pmis', ['ScopeOfWork'])

        # Adding model 'Planning'
        db.create_table(u'pmis_planning', (
            ('cid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, db_index=True)),
            ('vid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 14, 0, 0))),
            ('update_comment', self.gf('django.db.models.fields.TextField')()),
            ('update_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('month', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('planned_expanses', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('planned_progress', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='plannings', to=orm['pmis.Project'])),
        ))
        db.send_create_signal(u'pmis', ['Planning'])

        # Adding model 'Milestone'
        db.create_table(u'pmis_milestone', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phase', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('weeks_after_previous', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='milestones', to=orm['pmis.Project'])),
        ))
        db.send_create_signal(u'pmis', ['Milestone'])

        # Adding model 'ProjectMilestone'
        db.create_table(u'pmis_projectmilestone', (
            ('cid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, db_index=True)),
            ('vid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 14, 0, 0))),
            ('update_comment', self.gf('django.db.models.fields.TextField')()),
            ('update_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('completion_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 14, 0, 0))),
            ('milestone', self.gf('django.db.models.fields.related.ForeignKey')(related_name='project_milestone', to=orm['pmis.Milestone'])),
        ))
        db.send_create_signal(u'pmis', ['ProjectMilestone'])

        # Adding model 'CommentType'
        db.create_table(u'pmis_commenttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'pmis', ['CommentType'])

        # Adding model 'MonthlySubmission'
        db.create_table(u'pmis_monthlysubmission', (
            ('cid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, db_index=True)),
            ('vid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 14, 0, 0))),
            ('update_comment', self.gf('django.db.models.fields.TextField')()),
            ('update_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('month', self.gf('django.db.models.fields.DateField')()),
            ('current_milestone', self.gf('django.db.models.fields.related.ForeignKey')(related_name='monthly_submissions', to=orm['pmis.Milestone'])),
            ('actual_expenditure', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('actual_progress', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('comment_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='coment_types', to=orm['pmis.CommentType'])),
            ('remedial_action', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'pmis', ['MonthlySubmission'])


    def backwards(self, orm):
        # Deleting model 'Client'
        db.delete_table(u'pmis_client')

        # Deleting model 'Municipality'
        db.delete_table(u'pmis_municipality')

        # Deleting model 'District'
        db.delete_table(u'pmis_district')

        # Deleting model 'Programme'
        db.delete_table(u'pmis_programme')

        # Deleting model 'Project'
        db.delete_table(u'pmis_project')

        # Removing M2M table for field district on 'Project'
        db.delete_table('pmis_project_district')

        # Deleting model 'PeopleType'
        db.delete_table(u'pmis_peopletype')

        # Deleting model 'ProjectPeople'
        db.delete_table(u'pmis_projectpeople')

        # Removing M2M table for field people_type on 'ProjectPeople'
        db.delete_table('pmis_projectpeople_people_type')

        # Deleting model 'ProjectFinancial'
        db.delete_table(u'pmis_projectfinancial')

        # Deleting model 'Budget'
        db.delete_table(u'pmis_budget')

        # Deleting model 'ScopeCode'
        db.delete_table(u'pmis_scopecode')

        # Deleting model 'ScopeOfWork'
        db.delete_table(u'pmis_scopeofwork')

        # Deleting model 'Planning'
        db.delete_table(u'pmis_planning')

        # Deleting model 'Milestone'
        db.delete_table(u'pmis_milestone')

        # Deleting model 'ProjectMilestone'
        db.delete_table(u'pmis_projectmilestone')

        # Deleting model 'CommentType'
        db.delete_table(u'pmis_commenttype')

        # Deleting model 'MonthlySubmission'
        db.delete_table(u'pmis_monthlysubmission')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'pmis.budget': {
            'Meta': {'object_name': 'Budget'},
            'allocated_budget': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            'cid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'db_index': 'True'}),
            'project_financial': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'budgets'", 'to': u"orm['pmis.ProjectFinancial']"}),
            'update_comment': ('django.db.models.fields.TextField', [], {}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 14, 0, 0)'}),
            'update_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'vid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'year': ('django.db.models.fields.DateField', [], {})
        },
        u'pmis.client': {
            'Meta': {'object_name': 'Client'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'pmis.commenttype': {
            'Meta': {'object_name': 'CommentType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'pmis.district': {
            'Meta': {'object_name': 'District'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'municipality': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'districts'", 'to': u"orm['pmis.Municipality']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'pmis.milestone': {
            'Meta': {'object_name': 'Milestone'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'phase': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'milestones'", 'to': u"orm['pmis.Project']"}),
            'weeks_after_previous': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'pmis.monthlysubmission': {
            'Meta': {'object_name': 'MonthlySubmission'},
            'actual_expenditure': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'actual_progress': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'cid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'db_index': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'comment_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coment_types'", 'to': u"orm['pmis.CommentType']"}),
            'current_milestone': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'monthly_submissions'", 'to': u"orm['pmis.Milestone']"}),
            'month': ('django.db.models.fields.DateField', [], {}),
            'remedial_action': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'update_comment': ('django.db.models.fields.TextField', [], {}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 14, 0, 0)'}),
            'update_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'vid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'pmis.municipality': {
            'Meta': {'object_name': 'Municipality'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'pmis.peopletype': {
            'Meta': {'object_name': 'PeopleType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'pmis.planning': {
            'Meta': {'object_name': 'Planning'},
            'cid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'db_index': 'True'}),
            'month': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'planned_expanses': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'planned_progress': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'plannings'", 'to': u"orm['pmis.Project']"}),
            'update_comment': ('django.db.models.fields.TextField', [], {}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 14, 0, 0)'}),
            'update_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'vid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'pmis.programme': {
            'Meta': {'object_name': 'Programme'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'programmes'", 'to': u"orm['pmis.Client']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'pmis.project': {
            'Meta': {'object_name': 'Project'},
            'cid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'district': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'projects'", 'symmetrical': 'False', 'to': u"orm['pmis.District']"}),
            'municipality': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'to': u"orm['pmis.Municipality']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'programme': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'null': 'True', 'to': u"orm['pmis.Programme']"}),
            'update_comment': ('django.db.models.fields.TextField', [], {}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 14, 0, 0)'}),
            'update_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'vid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'pmis.projectfinancial': {
            'Meta': {'object_name': 'ProjectFinancial'},
            'cid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'db_index': 'True'}),
            'project': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pmis.Project']", 'unique': 'True'}),
            'project_planning_budget': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            'total_anticipated_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            'update_comment': ('django.db.models.fields.TextField', [], {}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 14, 0, 0)'}),
            'update_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'vid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'pmis.projectmilestone': {
            'Meta': {'object_name': 'ProjectMilestone'},
            'cid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'db_index': 'True'}),
            'completion_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 14, 0, 0)'}),
            'milestone': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_milestone'", 'to': u"orm['pmis.Milestone']"}),
            'update_comment': ('django.db.models.fields.TextField', [], {}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 14, 0, 0)'}),
            'update_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'vid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'pmis.projectpeople': {
            'Meta': {'object_name': 'ProjectPeople'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'people_type': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'project_peoples'", 'symmetrical': 'False', 'to': u"orm['pmis.PeopleType']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_peoples'", 'to': u"orm['pmis.Project']"})
        },
        u'pmis.scopecode': {
            'Meta': {'object_name': 'ScopeCode'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'pmis.scopeofwork': {
            'Meta': {'object_name': 'ScopeOfWork'},
            'cid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'db_index': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scope_of_works'", 'to': u"orm['pmis.Project']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'scope_code': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scope_of_works'", 'to': u"orm['pmis.ScopeCode']"}),
            'update_comment': ('django.db.models.fields.TextField', [], {}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 14, 0, 0)'}),
            'update_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'vid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['pmis']