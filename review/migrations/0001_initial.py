# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Review'
        db.create_table(u'review_review', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'review', ['Review'])

        # Adding model 'Schedule'
        db.create_table(u'review_schedule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('checked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('rate', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('review', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['review.Review'])),
        ))
        db.send_create_signal(u'review', ['Schedule'])

        # Adding model 'Question'
        db.create_table(u'review_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 9, 2, 0, 0))),
            ('review', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['review.Review'], null=True, blank=True)),
        ))
        db.send_create_signal(u'review', ['Question'])


    def backwards(self, orm):
        # Deleting model 'Review'
        db.delete_table(u'review_review')

        # Deleting model 'Schedule'
        db.delete_table(u'review_schedule')

        # Deleting model 'Question'
        db.delete_table(u'review_question')


    models = {
        u'review.question': {
            'Meta': {'object_name': 'Question'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'review': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['review.Review']", 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        u'review.review': {
            'Meta': {'object_name': 'Review'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'review.schedule': {
            'Meta': {'object_name': 'Schedule'},
            'checked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rate': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'review': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['review.Review']"})
        }
    }

    complete_apps = ['review']