''' Any function related to getCourses.py should be located here'''
from app.allImports import *
from app.logic import databaseInterface
#CREATE TWO DEFAULT DICTIONARIES
class GetCourses():
  '''Purpose: This class should hold any functions directly related to courses.py'''

  def __init__(self, user):
    self.username = user.get_username()

  def check_for_my_courses(self,SEID):
      '''Purpose: Checks to see if the user is teaching any courses'''

      # temp_courses = UsersCourses.get(UsersCourses.username == self.username)
      my_courses   = databaseInterface.grab_my_courses(self.username,SEID)
      return my_courses
