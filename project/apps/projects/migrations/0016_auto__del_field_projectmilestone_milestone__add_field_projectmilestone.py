# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ProjectMilestone.milestone'
        db.delete_column(u'projects_projectmilestone', 'milestone_id')

        # Adding field 'ProjectMilestone.project'
        db.add_column(u'projects_projectmilestone', 'project',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='project_milestone', to=orm['projects.Project']),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'ProjectMilestone.milestone'
        raise RuntimeError("Cannot reverse this migration. 'ProjectMilestone.milestone' and its values cannot be restored.")
        # Deleting field 'ProjectMilestone.project'
        db.delete_column(u'projects_projectmilestone', 'project_id')


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
            'actual_expenditure': ('django.db.models.fields.FloatField', [], {}),
            'actual_progress': ('django.db.models.fields.FloatField', [], {}),
            'cid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'db_index': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'comment_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'monthly_submissions'", 'to': u"orm['projects.CommentType']"}),
            'month': ('django.db.models.fields.CharField', [], {'default': '5', 'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'monthly_submissions'", 'to': u"orm['projects.Project']"}),
            'remedial_action': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'update_comment': ('django.db.models.fields.TextField', [], {}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 14, 0, 0)'}),
            'update_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'vid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'cid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'db_index': 'True'}),
            'month': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'planned_expenses': ('django.db.models.fields.FloatField', [], {}),
            'planned_progress': ('django.db.models.fields.FloatField', [], {}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'plannings'", 'to': u"orm['projects.Project']"}),
            'update_comment': ('django.db.models.fields.TextField', [], {}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 14, 0, 0)'}),
            'update_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'vid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'year': ('django.db.models.fields.CharField', [], {'default': '2013', 'max_length': '255'})
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
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_milestone'", 'to': u"orm['projects.Project']"}),
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
        u'projects.projectstatus': {
            'Meta': {'object_name': 'ProjectStatus'},
            'cid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'db_index': 'True'}),
            'project': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['projects.Project']", 'unique': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'update_comment': ('django.db.models.fields.TextField', [], {}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 14, 0, 0)'}),
            'update_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'vid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        },
        u'projects.varianceorder': {
            'Meta': {'object_name': 'VarianceOrder'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'cid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variance_orders'", 'to': u"orm['projects.Project']"}),
            'update_comment': ('django.db.models.fields.TextField', [], {}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 14, 0, 0)'}),
            'update_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'vid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['projects']