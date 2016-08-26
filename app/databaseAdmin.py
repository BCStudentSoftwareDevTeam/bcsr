from allImports import *
from flask_admin.contrib.peewee import ModelView

class AuthenticatedUser(ModelView):
    
    def is_accessible(self):
        return authUser(request.environ) == cfg['databaseAdmin']['user']
    
admin.add_view(AuthenticatedUser(Semesters))
admin.add_view(AuthenticatedUser(Divisions))
admin.add_view(AuthenticatedUser(Programs))
admin.add_view(AuthenticatedUser(Users))
admin.add_view(AuthenticatedUser(Courses))
admin.add_view(AuthenticatedUser(UsersCourses))
admin.add_view(AuthenticatedUser(Deadline))