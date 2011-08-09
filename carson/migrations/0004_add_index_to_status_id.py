# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding index on 'Tweet', fields ['status_id']
        db.create_index('carson_tweet', ['status_id'])


    def backwards(self, orm):
        
        # Removing index on 'Tweet', fields ['status_id']
        db.delete_index('carson_tweet', ['status_id'])


    models = {
        'carson.account': {
            'Meta': {'object_name': 'Account'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'twitter_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'twitter_username': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'carson.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'carson.tweet': {
            'Meta': {'ordering': "('-timestamp', '-status_id')", 'object_name': 'Tweet'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tweets'", 'null': 'True', 'to': "orm['carson.Account']"}),
            'data': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status_id': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['carson']
