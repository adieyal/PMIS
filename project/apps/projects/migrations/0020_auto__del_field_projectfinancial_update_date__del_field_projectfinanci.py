# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ProjectFinancial.update_date'
        db.delete_column(u'projects_projectfinancial', 'update_date')

        # Deleting field 'ProjectFinancial.update_user'
        db.delete_column(u'projects_projectfinancial', 'update_user_id')

        # Deleting field 'ProjectFinancial.vid'
        db.delete_column(u'projects_projectfinancial', 'vid')

        # Deleting field 'ProjectFinancial.update_comment'
        db.delete_column(u'projects_projectfinancial', 'update_comment')

        # Deleting field 'ProjectFinancial.cid'
        db.delete_column(u'projects_projectfinancial', 'cid')

        # Adding field 'ProjectFinancial.id'
        db.add_column(u'projects_projectfinancial', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=0, primary_key=True),
                      keep_default=False)

        # Deleting field 'MonthlySubmission.update_user'
        db.delete_column(u'projects_monthlysubmission', 'update_user_id')

        # Deleting field 'MonthlySubmission.update_comment'
        db.delete_column(u'projects_monthlysubmission', 'update_comment')

        # Deleting field 'MonthlySubmission.update_date'
        db.delete_column(u'projects_monthlysubmission', 'update_date')

        # Deleting field 'MonthlySubmission.vid'
        db.delete_column(u'projects_monthlysubmission', 'vid')

        # Deleting field 'MonthlySubmission.cid'
        db.delete_column(u'projects_monthlysubmission', 'cid')

        # Adding field 'MonthlySubmission.id'
        db.add_column(u'projects_monthlysubmission', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=0, primary_key=True),
                      keep_default=False)

        # Deleting field 'Budget.update_user'
        db.delete_column(u'projects_budget', 'update_user_id')

        # Deleting field 'Budget.vid'
        db.delete_column(u'projects_budget', 'vid')

        # Deleting field 'Budget.update_comment'
        db.delete_column(u'projects_budget', 'update_comment')

        # Deleting field 'Budget.cid'
        db.delete_column(u'projects_budget', 'cid')

        # Deleting field 'Budget.update_date'
        db.delete_column(u'projects_budget', 'update_date')

        # Adding field 'Budget.id'
        db.add_column(u'projects_budget', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=0, primary_key=True),
                      keep_default=False)

        # Deleting field 'ProjectMilestone.update_date'
        db.delete_column(u'projects_projectmilestone', 'update_date')

        # Deleting field 'ProjectMilestone.update_user'
        db.delete_column(u'projects_projectmilestone', 'update_user_id')

        # Deleting field 'ProjectMilestone.vid'
        db.delete_column(u'projects_projectmilestone', 'vid')

        # Deleting field 'ProjectMilestone.update_comment'
        db.delete_column(u'projects_projectmilestone', 'update_comment')

        # Deleting field 'ProjectMilestone.cid'
        db.delete_column(u'projects_projectmilestone', 'cid')

        # Adding field 'ProjectMilestone.id'
        db.add_column(u'projects_projectmilestone', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=0, primary_key=True),
                      keep_default=False)

        # Deleting field 'Planning.update_user'
        db.delete_column(u'projects_planning', 'update_user_id')

        # Deleting field 'Planning.vid'
        db.delete_column(u'projects_planning', 'vid')

        # Deleting field 'Planning.update_comment'
        db.delete_column(u'projects_planning', 'update_comment')

        # Deleting field 'Planning.update_date'
        db.delete_column(u'projects_planning', 'update_date')

        # Deleting field 'Planning.cid'
        db.delete_column(u'projects_planning', 'cid')

        # Adding field 'Planning.id'
        db.add_column(u'projects_planning', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=0, primary_key=True),
                      keep_default=False)

        # Deleting field 'ScopeOfWork.update_date'
        db.delete_column(u'projects_scopeofwork', 'update_date')

        # Deleting field 'ScopeOfWork.update_user'
        db.delete_column(u'projects_scopeofwork', 'update_user_id')

        # Deleting field 'ScopeOfWork.vid'
        db.delete_column(u'projects_scopeofwork', 'vid')

        # Deleting field 'ScopeOfWork.update_comment'
        db.delete_column(u'projects_scopeofwork', 'update_comment')

        # Deleting field 'ScopeOfWork.cid'
        db.delete_column(u'projects_scopeofwork', 'cid')

        # Adding field 'ScopeOfWork.id'
        db.add_column(u'projects_scopeofwork', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=0, primary_key=True),
                      keep_default=False)

        # Deleting field 'Project.update_date'
        db.delete_column(u'projects_project', 'update_date')

        # Deleting field 'Project.vid'
        db.delete_column(u'projects_project', 'vid')

        # Deleting field 'Project.update_user'
        db.delete_column(u'projects_project', 'update_user_id')

        # Deleting field 'Project.update_comment'
        db.delete_column(u'projects_project', 'update_comment')

        # Deleting field 'Project.cid'
        db.delete_column(u'projects_project', 'cid')

        # Adding field 'Project.id'
        db.add_column(u'projects_project', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=0, primary_key=True),
                      keep_default=False)

        # Deleting field 'VarianceOrder.update_date'
        db.delete_column(u'projects_varianceorder', 'update_date')

        # Deleting field 'VarianceOrder.update_user'
        db.delete_column(u'projects_varianceorder', 'update_user_id')

        # Deleting field 'VarianceOrder.update_comment'
        db.delete_column(u'projects_varianceorder', 'update_comment')

        # Deleting field 'VarianceOrder.cid'
        db.delete_column(u'projects_varianceorder', 'cid')

        # Deleting field 'VarianceOrder.vid'
        db.delete_column(u'projects_varianceorder', 'vid')

        # Adding field 'VarianceOrder.id'
        db.add_column(u'projects_varianceorder', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=0, primary_key=True),
                      keep_default=False)

        # Deleting field 'ProjectStatus.update_user'
        db.delete_column(u'projects_projectstatus', 'update_user_id')

        # Deleting field 'ProjectStatus.vid'
        db.delete_column(u'projects_projectstatus', 'vid')

        # Deleting field 'ProjectStatus.update_comment'
        db.delete_column(u'projects_projectstatus', 'update_comment')

        # Deleting field 'ProjectStatus.cid'
        db.delete_column(u'projects_projectstatus', 'cid')

        # Deleting field 'ProjectStatus.update_date'
        db.delete_column(u'projects_projectstatus', 'update_date')

        # Adding field 'ProjectStatus.id'
        db.add_column(u'projects_projectstatus', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=0, primary_key=True),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'ProjectFinancial.update_date'
        raise RuntimeError("Cannot reverse this migration. 'ProjectFinancial.update_date' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'ProjectFinancial.update_user'
        raise RuntimeError("Cannot reverse this migration. 'ProjectFinancial.update_user' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'ProjectFinancial.vid'
        raise RuntimeError("Cannot reverse this migration. 'ProjectFinancial.vid' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'ProjectFinancial.update_comment'
        raise RuntimeError("Cannot reverse this migration. 'ProjectFinancial.update_comment' and its values cannot be restored.")
        # Adding field 'ProjectFinancial.cid'
        db.add_column(u'projects_projectfinancial', 'cid',
                      self.gf('django.db.models.fields.CharField')(max_length=36, null=True, db_index=True),
                      keep_default=False)

        # Deleting field 'ProjectFinancial.id'
        db.delete_column(u'projects_projectfinancial', u'id')


        # User chose to not deal with backwards NULL issues for 'MonthlySubmission.update_user'
        raise RuntimeError("Cannot reverse this migration. 'MonthlySubmission.update_user' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'MonthlySubmission.update_comment'
        raise RuntimeError("Cannot reverse this migration. 'MonthlySubmission.update_comment' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'MonthlySubmission.update_date'
        raise RuntimeError("Cannot reverse this migration. 'MonthlySubmission.update_date' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'MonthlySubmission.vid'
        raise RuntimeError("Cannot reverse this migration. 'MonthlySubmission.vid' and its values cannot be restored.")
        # Adding field 'MonthlySubmission.cid'
        db.add_column(u'projects_monthlysubmission', 'cid',
                      self.gf('django.db.models.fields.CharField')(max_length=36, null=True, db_index=True),
                      keep_default=False)

        # Deleting field 'MonthlySubmission.id'
        db.delete_column(u'projects_monthlysubmission', u'id')


        # User chose to not deal with backwards NULL issues for 'Budget.update_user'
        raise RuntimeError("Cannot reverse this migration. 'Budget.update_user' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Budget.vid'
        raise RuntimeError("Cannot reverse this migration. 'Budget.vid' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Budget.update_comment'
        raise RuntimeError("Cannot reverse this migration. 'Budget.update_comment' and its values cannot be restored.")
        # Adding field 'Budget.cid'
        db.add_column(u'projects_budget', 'cid',
                      self.gf('django.db.models.fields.CharField')(max_length=36, null=True, db_index=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Budget.update_date'
        raise RuntimeError("Cannot reverse this migration. 'Budget.update_date' and its values cannot be restored.")
        # Deleting field 'Budget.id'
        db.delete_column(u'projects_budget', u'id')


        # User chose to not deal with backwards NULL issues for 'ProjectMilestone.update_date'
        raise RuntimeError("Cannot reverse this migration. 'ProjectMilestone.update_date' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'ProjectMilestone.update_user'
        raise RuntimeError("Cannot reverse this migration. 'ProjectMilestone.update_user' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'ProjectMilestone.vid'
        raise RuntimeError("Cannot reverse this migration. 'ProjectMilestone.vid' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'ProjectMilestone.update_comment'
        raise RuntimeError("Cannot reverse this migration. 'ProjectMilestone.update_comment' and its values cannot be restored.")
        # Adding field 'ProjectMilestone.cid'
        db.add_column(u'projects_projectmilestone', 'cid',
                      self.gf('django.db.models.fields.CharField')(max_length=36, null=True, db_index=True),
                      keep_default=False)

        # Deleting field 'ProjectMilestone.id'
        db.delete_column(u'projects_projectmilestone', u'id')


        # User chose to not deal with backwards NULL issues for 'Planning.update_user'
        raise RuntimeError("Cannot reverse this migration. 'Planning.update_user' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Planning.vid'
        raise RuntimeError("Cannot reverse this migration. 'Planning.vid' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Planning.update_comment'
        raise RuntimeError("Cannot reverse this migration. 'Planning.update_comment' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Planning.update_date'
        raise RuntimeError("Cannot reverse this migration. 'Planning.update_date' and its values cannot be restored.")
        # Adding field 'Planning.cid'
        db.add_column(u'projects_planning', 'cid',
                      self.gf('django.db.models.fields.CharField')(max_length=36, null=True, db_index=True),
                      keep_default=False)

        # Deleting field 'Planning.id'
        db.delete_column(u'projects_planning', u'id')


        # User chose to not deal with backwards NULL issues for 'ScopeOfWork.update_date'
        raise RuntimeError("Cannot reverse this migration. 'ScopeOfWork.update_date' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'ScopeOfWork.update_user'
        raise RuntimeError("Cannot reverse this migration. 'ScopeOfWork.update_user' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'ScopeOfWork.vid'
        raise RuntimeError("Cannot reverse this migration. 'ScopeOfWork.vid' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'ScopeOfWork.update_comment'
        raise RuntimeError("Cannot reverse this migration. 'ScopeOfWork.update_comment' and its values cannot be restored.")
        # Adding field 'ScopeOfWork.cid'
        db.add_column(u'projects_scopeofwork', 'cid',
                      self.gf('django.db.models.fields.CharField')(max_length=36, null=True, db_index=True),
                      keep_default=False)

        # Deleting field 'ScopeOfWork.id'
        db.delete_column(u'projects_scopeofwork', u'id')


        # User chose to not deal with backwards NULL issues for 'Project.update_date'
        raise RuntimeError("Cannot reverse this migration. 'Project.update_date' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Project.vid'
        raise RuntimeError("Cannot reverse this migration. 'Project.vid' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Project.update_user'
        raise RuntimeError("Cannot reverse this migration. 'Project.update_user' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Project.update_comment'
        raise RuntimeError("Cannot reverse this migration. 'Project.update_comment' and its values cannot be restored.")
        # Adding field 'Project.cid'
        db.add_column(u'projects_project', 'cid',
                      self.gf('django.db.models.fields.CharField')(max_length=36, null=True, db_index=True),
                      keep_default=False)

        # Deleting field 'Project.id'
        db.delete_column(u'projects_project', u'id')


        # User chose to not deal with backwards NULL issues for 'VarianceOrder.update_date'
        raise RuntimeError("Cannot reverse this migration. 'VarianceOrder.update_date' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'VarianceOrder.update_user'
        raise RuntimeError("Cannot reverse this migration. 'VarianceOrder.update_user' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'VarianceOrder.update_comment'
        raise RuntimeError("Cannot reverse this migration. 'VarianceOrder.update_comment' and its values cannot be restored.")
        # Adding field 'VarianceOrder.cid'
        db.add_column(u'projects_varianceorder', 'cid',
                      self.gf('django.db.models.fields.CharField')(max_length=36, null=True, db_index=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VarianceOrder.vid'
        raise RuntimeError("Cannot reverse this migration. 'VarianceOrder.vid' and its values cannot be restored.")
        # Deleting field 'VarianceOrder.id'
        db.delete_column(u'projects_varianceorder', u'id')


        # User chose to not deal with backwards NULL issues for 'ProjectStatus.update_user'
        raise RuntimeError("Cannot reverse this migration. 'ProjectStatus.update_user' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'ProjectStatus.vid'
        raise RuntimeError("Cannot reverse this migration. 'ProjectStatus.vid' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'ProjectStatus.update_comment'
        raise RuntimeError("Cannot reverse this migration. 'ProjectStatus.update_comment' and its values cannot be restored.")
        # Adding field 'ProjectStatus.cid'
        db.add_column(u'projects_projectstatus', 'cid',
                      self.gf('django.db.models.fields.CharField')(max_length=36, null=True, db_index=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ProjectStatus.update_date'
        raise RuntimeError("Cannot reverse this migration. 'ProjectStatus.update_date' and its values cannot be restored.")
        # Deleting field 'ProjectStatus.id'
        db.delete_column(u'projects_projectstatus', u'id')


    models = {
        u'projects.budget': {
            'Meta': {'object_name': 'Budget'},
            'allocated_budget': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project_financial': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'budgets'", 'to': u"orm['projects.ProjectFinancial']"}),
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
            'phase': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'projects.monthlysubmission': {
            'Meta': {'object_name': 'MonthlySubmission'},
            'actual_expenditure': ('django.db.models.fields.FloatField', [], {}),
            'actual_progress': ('django.db.models.fields.FloatField', [], {}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'comment_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'monthly_submissions'", 'to': u"orm['projects.CommentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.CharField', [], {'default': '5', 'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'monthly_submissions'", 'to': u"orm['projects.Project']"}),
            'remedial_action': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'projects.project': {
            'Meta': {'object_name': 'Project'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'municipality': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'projects'", 'symmetrical': 'False', 'to': u"orm['projects.Municipality']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'programme': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'null': 'True', 'to': u"orm['projects.Programme']"})
        },
        u'projects.projectfinancial': {
            'Meta': {'object_name': 'ProjectFinancial'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'project_financial'", 'unique': 'True', 'to': u"orm['projects.Project']"}),
            'project_planning_budget': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            'total_anticipated_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'})
        },
        u'projects.projectmilestone': {
            'Meta': {'object_name': 'ProjectMilestone'},
            'completion_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 17, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
        }
    }

    complete_apps = ['projects']