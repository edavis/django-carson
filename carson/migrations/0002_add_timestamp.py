# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Tweet.timestamp'
        db.add_column('carson_tweet', 'timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(1970, 1, 1)), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Tweet.timestamp'
        db.delete_column('carson_tweet', 'timestamp')


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
            'Meta': {'object_name': 'Tweet'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tweets'", 'null': 'True', 'to': "orm['carson.Account']"}),
            'data': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['carson']
