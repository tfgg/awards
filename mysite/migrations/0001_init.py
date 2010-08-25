
from south.db import db
from django.db import models
from mysite.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'RegisteredSite'
        db.create_table('mysite_registeredsite', (
            ('id', orm['mysite.RegisteredSite:id']),
            ('name', orm['mysite.RegisteredSite:name']),
            ('slug', orm['mysite.RegisteredSite:slug']),
            ('url', orm['mysite.RegisteredSite:url']),
            ('description', orm['mysite.RegisteredSite:description']),
            ('secret_key', orm['mysite.RegisteredSite:secret_key']),
        ))
        db.send_create_signal('mysite', ['RegisteredSite'])
        
        # Adding model 'Fingerprint'
        db.create_table('mysite_fingerprint', (
            ('id', orm['mysite.Fingerprint:id']),
            ('user', orm['mysite.Fingerprint:user']),
            ('print_type', orm['mysite.Fingerprint:print_type']),
            ('source', orm['mysite.Fingerprint:source']),
            ('data', orm['mysite.Fingerprint:data']),
        ))
        db.send_create_signal('mysite', ['Fingerprint'])
        
        # Adding model 'Award'
        db.create_table('mysite_award', (
            ('id', orm['mysite.Award:id']),
            ('name', orm['mysite.Award:name']),
            ('user', orm['mysite.Award:user']),
            ('date_awarded', orm['mysite.Award:date_awarded']),
            ('number', orm['mysite.Award:number']),
            ('source', orm['mysite.Award:source']),
            ('points_value', orm['mysite.Award:points_value']),
        ))
        db.send_create_signal('mysite', ['Award'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'RegisteredSite'
        db.delete_table('mysite_registeredsite')
        
        # Deleting model 'Fingerprint'
        db.delete_table('mysite_fingerprint')
        
        # Deleting model 'Award'
        db.delete_table('mysite_award')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mysite.award': {
            'date_awarded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'points_value': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mysite.RegisteredSite']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'mysite.fingerprint': {
            'data': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'print_type': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mysite.RegisteredSite']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'mysite.registeredsite': {
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'secret_key': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '80', 'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }
    
    complete_apps = ['mysite']
