# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Skill'
        db.create_table('skills_skill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
        ))
        db.send_create_signal('skills', ['Skill'])

        # Adding model 'Profile'
        db.create_table('skills_profile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('postcode', self.gf('django.db.models.fields.related.ForeignKey')(related_name='profiles', to=orm['geo.Postcode'])),
            ('posted', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('skills', ['Profile'])

        # Adding M2M table for field has_skills on 'Profile'
        db.create_table('skills_profile_has_skills', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('profile', models.ForeignKey(orm['skills.profile'], null=False)),
            ('skill', models.ForeignKey(orm['skills.skill'], null=False))
        ))
        db.create_unique('skills_profile_has_skills', ['profile_id', 'skill_id'])

        # Adding M2M table for field required_skills on 'Profile'
        db.create_table('skills_profile_required_skills', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('profile', models.ForeignKey(orm['skills.profile'], null=False)),
            ('skill', models.ForeignKey(orm['skills.skill'], null=False))
        ))
        db.create_unique('skills_profile_required_skills', ['profile_id', 'skill_id'])

        # Adding model 'Tweets'
        db.create_table('skills_tweets', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tweets', to=orm['skills.Profile'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('posted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('skills', ['Tweets'])


    def backwards(self, orm):
        
        # Deleting model 'Skill'
        db.delete_table('skills_skill')

        # Deleting model 'Profile'
        db.delete_table('skills_profile')

        # Removing M2M table for field has_skills on 'Profile'
        db.delete_table('skills_profile_has_skills')

        # Removing M2M table for field required_skills on 'Profile'
        db.delete_table('skills_profile_required_skills')

        # Deleting model 'Tweets'
        db.delete_table('skills_tweets')


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
        },
        'skills.profile': {
            'Meta': {'ordering': "('-posted',)", 'object_name': 'Profile'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'has_skills': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'doers'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['skills.Skill']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postcode': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'profiles'", 'to': "orm['geo.Postcode']"}),
            'posted': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'required_skills': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'seekers'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['skills.Skill']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'skills.skill': {
            'Meta': {'ordering': "('slug',)", 'object_name': 'Skill'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'skills.tweets': {
            'Meta': {'ordering': "('-posted',)", 'object_name': 'Tweets'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'posted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tweets'", 'to': "orm['skills.Profile']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        }
    }

    complete_apps = ['skills']
