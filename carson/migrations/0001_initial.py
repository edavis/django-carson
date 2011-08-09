# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Account'
        db.create_table('carson_account', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('twitter_username', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('twitter_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
        ))
        db.send_create_signal('carson', ['Account'])

        # Adding model 'Tag'
        db.create_table('carson_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal('carson', ['Tag'])

        # Adding model 'Tweet'
        db.create_table('carson_tweet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tweets', null=True, to=orm['carson.Account'])),
            ('data', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('carson', ['Tweet'])


    def backwards(self, orm):
        
        # Deleting model 'Account'
        db.delete_table('carson_account')

        # Deleting model 'Tag'
        db.delete_table('carson_tag')

        # Deleting model 'Tweet'
        db.delete_table('carson_tweet')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['carson']
