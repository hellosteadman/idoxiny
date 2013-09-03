from django.contrib import admin
from idoxiny.skills.models import Skill, Profile

class SkillAdmin(admin.ModelAdmin):
	pass

admin.site.register(Skill, SkillAdmin)

class ProfileAdmin(admin.ModelAdmin):
	list_display = ('username', 'postcode', 'posted')
	list_filter = ('has_skills', 'required_skills')
	date_hierarchy = 'posted'
	readonly_fields = ('username', 'posted')

admin.site.register(Profile, ProfileAdmin)