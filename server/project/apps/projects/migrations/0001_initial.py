# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Versioned'
        db.create_table(u'projects_versioned', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('revision', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['reversion.Revision'], unique=True)),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('update_comment', self.gf('django.db.models.fields.TextField')()),
            ('update_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'projects', ['Versioned'])

        # Adding model 'Client'
        db.create_table(u'projects_client', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'projects', ['Client'])

        # Adding model 'District'
        db.create_table(u'projects_district', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'projects', ['District'])

        # Adding model 'Municipality'
        db.create_table(u'projects_municipality', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('district', self.gf('django.db.models.fields.related.ForeignKey')(related_name='municipalities', to=orm['projects.District'])),
        ))
        db.send_create_signal(u'projects', ['Municipality'])

        # Adding model 'Programme'
        db.create_table(u'projects_programme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(related_name='programmes', to=orm['projects.Client'])),
        ))
        db.send_create_signal(u'projects', ['Programme'])

        # Adding model 'Project'
        db.create_table(u'projects_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('project_number', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('programme', self.gf('django.db.models.fields.related.ForeignKey')(related_name='projects', null=True, to=orm['projects.Programme'])),
        ))
        db.send_create_signal(u'projects', ['Project'])

        # Adding M2M table for field municipality on 'Project'
        db.create_table(u'projects_project_municipality', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'projects.project'], null=False)),
            ('municipality', models.ForeignKey(orm[u'projects.municipality'], null=False))
        ))
        db.create_unique(u'projects_project_municipality', ['project_id', 'municipality_id'])

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
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('total_anticipated_cost', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2)),
            ('project', self.gf('django.db.models.fields.related.OneToOneField')(related_name='project_financial', unique=True, to=orm['projects.Project'])),
        ))
        db.send_create_signal(u'projects', ['ProjectFinancial'])

        # Adding model 'Budget'
        db.create_table(u'projects_budget', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('year', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('allocated_budget', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2)),
            ('allocated_planning_budget', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2)),
            ('project', self.gf('django.db.models.fields.related.OneToOneField')(related_name='budgets', unique=True, to=orm['projects.Project'])),
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
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('scope_code', self.gf('django.db.models.fields.related.ForeignKey')(related_name='scope_of_works', to=orm['projects.ScopeCode'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='scope_of_works', to=orm['projects.Project'])),
        ))
        db.send_create_signal(u'projects', ['ScopeOfWork'])

        # Adding model 'Planning'
        db.create_table(u'projects_planning', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('month', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('year', self.gf('django.db.models.fields.CharField')(default=2013, max_length=255)),
            ('planned_expenses', self.gf('django.db.models.fields.FloatField')()),
            ('planned_progress', self.gf('django.db.models.fields.FloatField')()),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='plannings', to=orm['projects.Project'])),
        ))
        db.send_create_signal(u'projects', ['Planning'])

        # Adding model 'Milestone'
        db.create_table(u'projects_milestone', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phase', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'projects', ['Milestone'])

        # Adding model 'ProjectMilestone'
        db.create_table(u'projects_projectmilestone', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('completion_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 22, 0, 0))),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='project_milestone', to=orm['projects.Project'])),
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
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('month', self.gf('django.db.models.fields.CharField')(default=5, max_length=255)),
            ('year', self.gf('django.db.models.fields.CharField')(default=2013, max_length=255)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='monthly_submissions', to=orm['projects.Project'])),
            ('actual_expenditure', self.gf('django.db.models.fields.FloatField')()),
            ('actual_progress', self.gf('django.db.models.fields.FloatField')()),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('comment_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='monthly_submissions', null=True, to=orm['projects.CommentType'])),
            ('remedial_action', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'projects', ['MonthlySubmission'])

        # Adding model 'ProjectStatus'
        db.create_table(u'projects_projectstatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['projects.Project'], unique=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'projects', ['ProjectStatus'])

        # Adding model 'VarianceOrder'
        db.create_table(u'projects_varianceorder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='variance_orders', to=orm['projects.Project'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'projects', ['VarianceOrder'])

        # Adding model 'GroupPerm'
        db.create_table(u'projects_groupperm', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'projects', ['GroupPerm'])

        # Adding M2M table for field user on 'GroupPerm'
        db.create_table(u'projects_groupperm_user', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('groupperm', models.ForeignKey(orm[u'projects.groupperm'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(u'projects_groupperm_user', ['groupperm_id', 'user_id'])

        # Adding model 'GroupPermObj'
        db.create_table(u'projects_grouppermobj', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'projects', ['GroupPermObj'])

        # Adding M2M table for field group_perm on 'GroupPermObj'
        db.create_table(u'projects_grouppermobj_group_perm', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('grouppermobj', models.ForeignKey(orm[u'projects.grouppermobj'], null=False)),
            ('groupperm', models.ForeignKey(orm[u'projects.groupperm'], null=False))
        ))
        db.create_unique(u'projects_grouppermobj_group_perm', ['grouppermobj_id', 'groupperm_id'])

        # Adding M2M table for field project on 'GroupPermObj'
        db.create_table(u'projects_grouppermobj_project', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('grouppermobj', models.ForeignKey(orm[u'projects.grouppermobj'], null=False)),
            ('project', models.ForeignKey(orm[u'projects.project'], null=False))
        ))
        db.create_unique(u'projects_grouppermobj_project', ['grouppermobj_id', 'project_id'])


    def backwards(self, orm):
        # Deleting model 'Versioned'
        db.delete_table(u'projects_versioned')

        # Deleting model 'Client'
        db.delete_table(u'projects_client')

        # Deleting model 'District'
        db.delete_table(u'projects_district')

        # Deleting model 'Municipality'
        db.delete_table(u'projects_municipality')

        # Deleting model 'Programme'
        db.delete_table(u'projects_programme')

        # Deleting model 'Project'
        db.delete_table(u'projects_project')

        # Removing M2M table for field municipality on 'Project'
        db.delete_table('projects_project_municipality')

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

        # Deleting model 'ProjectStatus'
        db.delete_table(u'projects_projectstatus')

        # Deleting model 'VarianceOrder'
        db.delete_table(u'projects_varianceorder')

        # Deleting model 'GroupPerm'
        db.delete_table(u'projects_groupperm')

        # Removing M2M table for field user on 'GroupPerm'
        db.delete_table('projects_groupperm_user')

        # Deleting model 'GroupPermObj'
        db.delete_table(u'projects_grouppermobj')

        # Removing M2M table for field group_perm on 'GroupPermObj'
        db.delete_table('projects_grouppermobj_group_perm')

        # Removing M2M table for field project on 'GroupPermObj'
        db.delete_table('projects_grouppermobj_project')


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
            'allocated_planning_budget': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'budgets'", 'unique': 'True', 'to': u"orm['projects.Project']"}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'projects.client': {
            'Meta': {'object_name': 'Client'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
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
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'projects.entity': {
            'Meta': {'object_name': 'Entity'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'projects.groupperm': {
            'Meta': {'object_name': 'GroupPerm'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'group_perms'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"})
        },
        u'projects.grouppermobj': {
            'Meta': {'object_name': 'GroupPermObj'},
            'group_perm': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'group_perm_objs'", 'symmetrical': 'False', 'to': u"orm['projects.GroupPerm']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'group_perm_objs'", 'symmetrical': 'False', 'to': u"orm['projects.Project']"})
        },
        u'projects.milestone': {
            'Meta': {'object_name': 'Milestone'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'phase': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'projects.monthlysubmission': {
            'Meta': {'object_name': 'MonthlySubmission'},
            'actual_expenditure': ('django.db.models.fields.FloatField', [], {}),
            'actual_progress': ('django.db.models.fields.FloatField', [], {}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'comment_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'monthly_submissions'", 'null': 'True', 'to': u"orm['projects.CommentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.CharField', [], {'default': '5', 'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'monthly_submissions'", 'to': u"orm['projects.Project']"}),
            'remedial_action': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'year': ('django.db.models.fields.CharField', [], {'default': '2013', 'max_length': '255'})
        },
        u'projects.municipality': {
            'Meta': {'object_name': 'Municipality'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'municipalities'", 'to': u"orm['projects.District']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'projects.planning': {
            'Meta': {'object_name': 'Planning'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'planned_expenses': ('django.db.models.fields.FloatField', [], {}),
            'planned_progress': ('django.db.models.fields.FloatField', [], {}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'plannings'", 'to': u"orm['projects.Project']"}),
            'year': ('django.db.models.fields.CharField', [], {'default': '2013', 'max_length': '255'})
        },
        u'projects.programme': {
            'Meta': {'object_name': 'Programme'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'programmes'", 'to': u"orm['projects.Client']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'projects.project': {
            'Meta': {'object_name': 'Project'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'municipality': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'projects'", 'symmetrical': 'False', 'to': u"orm['projects.Municipality']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'programme': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'null': 'True', 'to': u"orm['projects.Programme']"}),
            'project_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
        },
        u'projects.projectfinancial': {
            'Meta': {'object_name': 'ProjectFinancial'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'project_financial'", 'unique': 'True', 'to': u"orm['projects.Project']"}),
            'total_anticipated_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'})
        },
        u'projects.projectmilestone': {
            'Meta': {'object_name': 'ProjectMilestone'},
            'completion_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 22, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'milestone': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_milestone'", 'to': u"orm['projects.Milestone']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_milestone'", 'to': u"orm['projects.Project']"})
        },
        u'projects.projectrole': {
            'Meta': {'object_name': 'ProjectRole'},
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_roles'", 'to': u"orm['projects.Entity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_roles'", 'to': u"orm['projects.Project']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_roles'", 'to': u"orm['projects.Role']"})
        },
        u'projects.projectstatus': {
            'Meta': {'object_name': 'ProjectStatus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['projects.Project']", 'unique': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scope_of_works'", 'to': u"orm['projects.Project']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'scope_code': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scope_of_works'", 'to': u"orm['projects.ScopeCode']"})
        },
        u'projects.varianceorder': {
            'Meta': {'object_name': 'VarianceOrder'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variance_orders'", 'to': u"orm['projects.Project']"})
        },
        u'projects.versioned': {
            'Meta': {'object_name': 'Versioned'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'revision': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['reversion.Revision']", 'unique': 'True'}),
            'update_comment': ('django.db.models.fields.TextField', [], {}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'update_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'reversion.revision': {
            'Meta': {'object_name': 'Revision'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manager_slug': ('django.db.models.fields.CharField', [], {'default': "u'default'", 'max_length': '200', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['projects']