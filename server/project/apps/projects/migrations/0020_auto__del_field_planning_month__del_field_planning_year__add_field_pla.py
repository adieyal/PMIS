# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'MonthlySubmission', fields ['project', 'year', 'month']
        db.delete_unique(u'projects_monthlysubmission', ['project_id', 'year', 'month'])

        # Removing unique constraint on 'Planning', fields ['project', 'year', 'month']
        db.delete_unique(u'projects_planning', ['project_id', 'year', 'month'])

        # Deleting field 'Planning.month'
        db.delete_column(u'projects_planning', 'month')

        # Deleting field 'Planning.year'
        db.delete_column(u'projects_planning', 'year')

        # Adding field 'Planning.date'
        db.add_column(u'projects_planning', 'date',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 6, 0, 0)),
                      keep_default=False)

        # Deleting field 'MonthlySubmission.year'
        db.delete_column(u'projects_monthlysubmission', 'year')

        # Deleting field 'MonthlySubmission.month'
        db.delete_column(u'projects_monthlysubmission', 'month')

        # Adding field 'MonthlySubmission.date'
        db.add_column(u'projects_monthlysubmission', 'date',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 6, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Planning.month'
        raise RuntimeError("Cannot reverse this migration. 'Planning.month' and its values cannot be restored.")
        # Adding field 'Planning.year'
        db.add_column(u'projects_planning', 'year',
                      self.gf('django.db.models.fields.CharField')(default=2013, max_length=255),
                      keep_default=False)

        # Deleting field 'Planning.date'
        db.delete_column(u'projects_planning', 'date')

        # Adding unique constraint on 'Planning', fields ['project', 'year', 'month']
        db.create_unique(u'projects_planning', ['project_id', 'year', 'month'])

        # Adding field 'MonthlySubmission.year'
        db.add_column(u'projects_monthlysubmission', 'year',
                      self.gf('django.db.models.fields.CharField')(default=2013, max_length=255),
                      keep_default=False)

        # Adding field 'MonthlySubmission.month'
        db.add_column(u'projects_monthlysubmission', 'month',
                      self.gf('django.db.models.fields.CharField')(default=7, max_length=255),
                      keep_default=False)

        # Deleting field 'MonthlySubmission.date'
        db.delete_column(u'projects_monthlysubmission', 'date')

        # Adding unique constraint on 'MonthlySubmission', fields ['project', 'year', 'month']
        db.create_unique(u'projects_monthlysubmission', ['project_id', 'year', 'month'])


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
            'Meta': {'unique_together': "(('year', 'project'),)", 'object_name': 'Budget'},
            'allocated_budget': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '2', 'blank': 'True'}),
            'allocated_planning_budget': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'budgets'", 'to': u"orm['projects.Project']"}),
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
            'Meta': {'unique_together': "(('phase', 'order'),)", 'object_name': 'Milestone'},
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
            'comment_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'submissions'", 'null': 'True', 'to': u"orm['projects.CommentType']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'monthly_submissions'", 'to': u"orm['projects.Project']"}),
            'remedial_action': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
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
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'planned_expenses': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'planned_progress': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'plannings'", 'to': u"orm['projects.Project']"})
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
            'current_step': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Milestone']", 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'municipality': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'null': 'True', 'to': u"orm['projects.Municipality']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'programme': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'null': 'True', 'to': u"orm['projects.Programme']"}),
            'project_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
        },
        u'projects.projectfinancial': {
            'Meta': {'object_name': 'ProjectFinancial'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'project_financial'", 'unique': 'True', 'to': u"orm['projects.Project']"}),
            'total_anticipated_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '2', 'blank': 'True'})
        },
        u'projects.projectmilestone': {
            'Meta': {'object_name': 'ProjectMilestone'},
            'completion_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'milestone': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_milestone'", 'to': u"orm['projects.Milestone']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'milestones'", 'to': u"orm['projects.Project']"})
        },
        u'projects.projectrole': {
            'Meta': {'object_name': 'ProjectRole'},
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'project_roles'", 'null': 'True', 'to': u"orm['projects.Entity']"}),
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
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'projects.scopeofwork': {
            'Meta': {'object_name': 'ScopeOfWork'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scope_of_works'", 'to': u"orm['projects.Project']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
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
            'revision': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'versioned'", 'unique': 'True', 'to': u"orm['reversion.Revision']"}),
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