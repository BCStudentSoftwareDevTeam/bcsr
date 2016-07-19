'''
Purpose Of File: To hold all of the functions for app.courses
'''
from app.allImports import *
from app.logic import databaseInterface  
#CREATE TWO DEFAULT DICTIONARIES
class GetCourses():
  def __init__(self):
    #self.username = authUser(request.environ)
    self.username = 'heggens'
 
  def create_dictionaries(self):
    #divsionsToPrograms will contain a mapping of semesters the divisions to the programs
    divisions_to_programs     = {} 
    #programsToCourses will contain a mapping of programs to the courses in the program. 
    programs_to_courses       = {} 
    divisions = databaseInterface.grab_all_divisions()
    for division in divisions:
      programs = databaseInterface.grab_programs_in_division(division.DID)
      divisions_to_programs[division.name] = programs
    for program in programs:
      courses = databaseInterface.grab_courses_in_program(program.PID)
      programs_to_courses[program.name] = courses
    return(divisions_to_programs,programs_to_courses)
    
  def check_for_my_courses(self):
    try: 
      temp_courses = UsersCourses.get(UsersCourses.username == self.username)
      my_courses   = databaseInterface.grab_my_courses(self.username)
    except DoesNotExist:
      my_courses = None
    return my_courses
      