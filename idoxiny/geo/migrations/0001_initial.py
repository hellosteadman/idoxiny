# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Postcode'
        db.create_table('geo_postcode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('postcode', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(related_name='postcodes', to=orm['geo.Area'])),
            ('latitude', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('longitude', self.gf('django.db.models.fields.CharField')(max_length=36)),
        ))
        db.send_create_signal('geo', ['Postcode'])

        # Adding model 'Area'
        db.create_table('geo_area', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100, db_index=True)),
        ))
        db.send_create_signal('geo', ['Area'])


    def backwards(self, orm):
        
        # Deleting model 'Postcode'
        db.delete_table('geo_postcode')

        # Deleting model 'Area'
        db.delete_table('geo_area')


    models = {
        'geo.area': {
            'Meta': {'ordering': "('slug',)", 'object_name': 'Area'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'geo.postcode': {
            'Meta': {'ordering': "('postcode',)", 'object_name': 'Postcode'},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'postcodes'", 'to': "orm['geo.Area']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'postcode': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
        }
    }

    complete_apps = ['geo']
