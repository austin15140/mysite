# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Poll.comments'
        db.add_column(u'polls_poll', 'comments',
                      self.gf('django.db.models.fields.CharField')(default='Write something witty', max_length=800),
                      keep_default=False)


        # Changing field 'Poll.image'
        db.alter_column(u'polls_poll', 'image', self.gf('django.db.models.fields.files.ImageField')(max_length=100))

    def backwards(self, orm):
        # Deleting field 'Poll.comments'
        db.delete_column(u'polls_poll', 'comments')


        # Changing field 'Poll.image'
        db.alter_column(u'polls_poll', 'image', self.gf('django.db.models.fields.files.FileField')(max_length=100))

    models = {
        u'polls.choice': {
            'Meta': {'object_name': 'Choice'},
            'choice_text': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polls.Poll']"}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'polls.poll': {
            'Meta': {'object_name': 'Poll'},
            'comments': ('django.db.models.fields.CharField', [], {'default': "'Write something witty'", 'max_length': '800'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['polls']