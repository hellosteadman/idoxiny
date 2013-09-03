from django.db.models import Manager

class ProfileManager(Manager):
	def get_query_set(self):
		return self.model.QuerySet(self.model)
		
	def near(self, latitude, longitude):
		return self.get_query_set().near(latitude, longitude)

class SkillManager(Manager):
	def get_query_set(self):
		return self.model.QuerySet(self.model)
		
	def cloud(self):
		return self.get_query_set().cloud()