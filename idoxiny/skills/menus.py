from bambu import navigation

class SkillsMenuBuilder(navigation.MenuBuilder):
	def register_partials(self):
		return (
			{
				'name': 'skills',
				'description': 'Links to skills pages'
			},
		)
	
	def add_to_menu(self, name, items, **kwargs):
		items.append(
			{
				'url': ('skills',),
				'title': u'Skills',
				'selection': u'skills'
			}
		)
		
navigation.site.register(SkillsMenuBuilder)