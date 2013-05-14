# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Client'
        db.create_table(u'projects_client', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'projects', ['Client'])

        # Adding model 'Municipality'
        db.create_table(u'projects_municipality', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'projects', ['Municipality'])

        # Adding model 'District'
        db.create_table(u'projects_district', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('municipality', self.gf('django.db.models.fields.related.ForeignKey')(related_name='districts', to=orm['projects.Municipality'])),
        ))
        db.send_create_signal(u'projects', ['District'])

        # Adding model 'Programme'
        db.create_table(u'projects_programme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(related_name='programmes', to=orm['projects.Client'])),
        ))
        db.send_create_signal(u'projects', ['Programme'])

        # Adding model 'Project'
        db.create_table(u'projects_project', (
            ('cid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, db_index=True)),
            ('vid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 14, 0, 0))),
            ('update_comment', self.gf('django.db.models.fields.TextField')()),
            ('update_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('programme', self.gf('django.db.models.fields.related.ForeignKey')(related_name='projects', null=True, to=orm['projects.Programme'])),
            ('municipality', self.gf('django.db.models.fields.related.ForeignKey')(related_name='projects', to=orm['projects.Municipality'])),
        ))
        db.send_create_signal(u'projects', ['Project'])

        # Adding M2M table for field district on 'Project'
        db.create_table(u'projects_project_district', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'projects.project'], null=False)),
            ('district', models.ForeignKey(orm[u'projects.district'], null=False))
        ))
        db.create_unique(u'projects_project_district', ['project_id', 'district_id'])

        # Adding model 'Entity'
        db.create_table(u'projects_entity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'projects', ['Entity'])

        # Adding model 'Role'
        db.create_table(u'projects_role', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'projects', ['Role'])

        # Adding model 'ProjectRole'
        db.create_table(u'projects_projectrole', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='project_roles', to=orm['projects.Project'])),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(related_name='project_roles', to=orm['projects.Role'])),
            ('entity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='project_roles', to=orm['projects.Entity'])),
        ))
        db.send_create_signal(u'projects', ['ProjectRole'])

        # Adding model 'ProjectFinancial'
        db.create_table(u'projects_projectfinancial', (
            ('cid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, db_index=True)),
            ('vid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 14, 0, 0))),
            ('update_comment', self.gf('django.db.models.fields.TextField')()),
            ('update_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('total_anticipated_cost', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2)),
            ('project_planning_budget', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2)),
            ('project', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['projects.Project'], unique=True)),
        ))
        db.send_create_signal(u'projects', ['ProjectFinancial'])

        # Adding model 'Budget'
        db.create_table(u'projects_budget', (
            ('cid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, db_index=True)),
            ('vid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 14, 0, 0))),
            ('update_comment', self.gf('django.db.models.fields.TextField')()),
            ('update_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('year', self.gf('django.db.models.fields.DateField')()),
            ('allocated_budget', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2)),
            ('project_financial', self.gf('django.db.models.fields.related.ForeignKey')(related_name='budgets', to=orm['projects.ProjectFinancial'])),
        ))
        db.send_create_signal(u'projects', ['Budget'])

        # Adding model 'ScopeCode'
        db.create_table(u'projects_scopecode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'projects', ['ScopeCode'])

        # Adding model 'ScopeOfWork'
        db.create_table(u'projects_scopeofwork', (
            ('cid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, db_index=True)),
            ('vid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 14, 0, 0))),
            ('update_comment', self.gf('django.db.models.fields.TextField')()),
            ('update_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('scope_code', self.gf('django.db.models.fields.related.ForeignKey')(related_name='scope_of_works', to=orm['projects.ScopeCode'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='scope_of_works', to=orm['projects.Project'])),
        ))
        db.send_create_signal(u'projects', ['ScopeOfWork'])

        # Adding model 'Planning'
        db.create_table(u'projects_planning', (
            ('cid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, db_index=True)),
            ('vid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 14, 0, 0))),
            ('update_comment', self.gf('django.db.models.fields.TextField')()),
            ('update_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('month', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('planned_expanses', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('planned_progress', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='plannings', to=orm['projects.Project'])),
        ))
        db.send_create_signal(u'projects', ['Planning'])

        # Adding model 'Milestone'
        db.create_table(u'projects_milestone', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phase', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('weeks_after_previous', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='milestones', to=orm['projects.Project'])),
        ))
        db.send_create_signal(u'projects', ['Milestone'])

        # Adding model 'ProjectMilestone'
        db.create_table(u'projects_projectmilestone', (
            ('cid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, db_index=True)),
            ('vid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 14, 0, 0))),
            ('update_comment', self.gf('django.db.models.fields.TextField')()),
            ('update_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('completion_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 14, 0, 0))),
            ('milestone', self.gf('django.db.models.fields.related.ForeignKey')(related_name='project_milestone', to=orm['projects.Milestone'])),
        ))
        db.send_create_signal(u'projects', ['ProjectMilestone'])

        # Adding model 'CommentType'
        db.create_table(u'projects_commenttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'projects', ['CommentType'])

        # Adding model 'MonthlySubmission'
        db.create_table(u'projects_monthlysubmission', (
            ('cid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, db_index=True)),
            ('vid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 14, 0, 0))),
            ('update_comment', self.gf('django.db.models.fields.TextField')()),
            ('update_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('month', self.gf('django.db.models.fields.DateField')()),
            ('current_milestone', self.gf('django.db.models.fields.related.ForeignKey')(related_name='monthly_submissions', to=orm['projects.Milestone'])),
            ('actual_expenditure', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('actual_progress', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('comment_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='coment_types', to=orm['projects.CommentType'])),
            ('remedial_action', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'projects', ['MonthlySubmission'])


    def backwards(self, orm):
        # Deleting model 'Client'
        db.delete_table(u'projects_client')

        # Deleting model 'Municipality'
        db.delete_table(u'projects_municipality')

        # Deleting model 'District'
        db.delete_table(u'projects_district')

        # Deleting model 'Programme'
        db.delete_table(u'projects_programme')

        # Deleting model 'Project'
        db.delete_table(u'projects_project')

        # Removing M2M table for field district on 'Project'
        db.delete_table('projects_project_district')

        # Deleting model 'Entity'
        db.delete_table(u'projects_entity')

        # Deleting model 'Role'
        db.delete_table(u'projects_role')

        # Deleting model 'ProjectRole'
        db.delete_table(u'projects_projectrole')

        # Deleting model 'ProjectFinancial'
        db.delete_table(u'projects_projectfinancial')

        # Deleting model 'Budget'
        db.delete_table(u'projects_budget')

        # Deleting model 'ScopeCode'
        db.delete_table(u'projects_scopecode')

        # Deleting model 'ScopeOfWork'
        db.delete_table(u'projects_scopeofwork')

        # Deleting model 'Planning'
        db.delete_table(u'projects_planning')

        # Deleting model 'Milestone'
        db.delete_table(u'projects_milestone')

        # Deleting model 'ProjectMilestone'
        db.delete_table(u'projects_projectmilestone')

        # Deleting model 'CommentType'
        db.delete_table(u'projects_commenttype')

        # Deleting model 'MonthlySubmission'
        db.delete_table(u'projects_monthlysubmission')


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
        u'projects.budget': {
            'Meta': {'object_name': 'Budget'},
            'allocated_budget': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            'cid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'db_index': 'True'}),
            'project_financial': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'budgets'", 'to': u"orm['projects.ProjectFinancial']"}),
            'update_comment': ('django.db.models.fields.TextField', [], {}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 14, 0, 0)'}),
            'update_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'vid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'year': ('django.db.models.fields.DateField', [], {})
        },
        u'projects.client': {
            'Meta': {'object_name': 'Client'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'projects.commenttype': {
            'Meta': {'object_name': 'CommentType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'projects.district': {
            'Meta': {'object_name': 'District'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'municipality': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'districts'", 'to': u"orm['projects.Municipality']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'projects.entity': {
            'Meta': {'object_name': 'Entity'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'projects.milestone': {
            'Meta': {'object_name': 'Milestone'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'phase': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'milestones'", 'to': u"orm['projects.Project']"}),
            'weeks_after_previous': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'projects.monthlysubmission': {
            'Meta': {'object_name': 'MonthlySubmission'},
            'actual_expenditure': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'actual_progress': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'cid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'db_index': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'comment_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coment_types'", 'to': u"orm['projects.CommentType']"}),
            'current_milestone': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'monthly_submissions'", 'to': u"orm['projects.Milestone']"}),
            'month': ('django.db.models.fields.DateField', [], {}),
            'remedial_action': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'update_comment': ('django.db.models.fields.TextField', [], {}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 14, 0, 0)'}),
            'update_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'vid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'projects.municipality': {
            'Meta': {'object_name': 'Municipality'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'projects.planning': {
            'Meta': {'object_name': 'Planning'},
            'cid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'db_index': 'True'}),
            'month': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'planned_expanses': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'planned_progress': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'plannings'", 'to': u"orm['projects.Project']"}),
            'update_comment': ('django.db.models.fields.TextField', [], {}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 14, 0, 0)'}),
            'update_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'vid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'projects.programme': {
            'Meta': {'object_name': 'Programme'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'programmes'", 'to': u"orm['projects.Client']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'projects.project': {
            'Meta': {'object_name': 'Project'},
            'cid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'district': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'projects'", 'symmetrical': 'False', 'to': u"orm['projects.District']"}),
            'municipality': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'to': u"orm['projects.Municipality']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'programme': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'null': 'True', 'to': u"orm['projects.Programme']"}),
            'update_comment': ('django.db.models.fields.TextField', [], {}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 14, 0, 0)'}),
            'update_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'vid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'projects.projectfinancial': {
            'Meta': {'object_name': 'ProjectFinancial'},
            'cid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'db_index': 'True'}),
            'project': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['projects.Project']", 'unique': 'True'}),
            'project_planning_budget': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            'total_anticipated_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            'update_comment': ('django.db.models.fields.TextField', [], {}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 14, 0, 0)'}),
            'update_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'vid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'projects.projectmilestone': {
            'Meta': {'object_name': 'ProjectMilestone'},
            'cid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'db_index': 'True'}),
            'completion_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 14, 0, 0)'}),
            'milestone': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_milestone'", 'to': u"orm['projects.Milestone']"}),
            'update_comment': ('django.db.models.fields.TextField', [], {}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 14, 0, 0)'}),
            'update_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'vid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'projects.projectrole': {
            'Meta': {'object_name': 'ProjectRole'},
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_roles'", 'to': u"orm['projects.Entity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_roles'", 'to': u"orm['projects.Project']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_roles'", 'to': u"orm['projects.Role']"})
        },
        u'projects.role': {
            'Meta': {'object_name': 'Role'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'projects.scopecode': {
            'Meta': {'object_name': 'ScopeCode'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'projects.scopeofwork': {
            'Meta': {'object_name': 'ScopeOfWork'},
            'cid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'db_index': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scope_of_works'", 'to': u"orm['projects.Project']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'scope_code': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scope_of_works'", 'to': u"orm['projects.ScopeCode']"}),
            'update_comment': ('django.db.models.fields.TextField', [], {}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 14, 0, 0)'}),
            'update_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'vid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['projects']