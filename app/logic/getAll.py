from app.allImports import *
from app.logic import databaseInterface

class GetAll():
  '''Purpose: This class should hold any methods that are used on multiple .py
  files. That way we know that anytime we make changes to one of these functions
  it will affect multiple files.'''
  def __init__(self):
    #self.username = authUser(request.environ)
    self.username = 'heggens'

  def create_dictionaries(self,SEID):
      '''Purpose: Creates a mapping using dictionaries of 1)divisions to programs
      2) programs to courses. -> Author : CDM 20160720
      @param SEID {integer} - number identification of semester peewee obj '''
      divisions_to_programs     = {}
      programs_to_courses       = {} 
      divisions = databaseInterface.grab_all_divisions()
      for division in divisions:
        programs = databaseInterface.grab_programs_in_division(division.DID)
        divisions_to_programs[division] = programs
        for program in programs:
          courses = databaseInterface.grab_courses_in_program(program.PID,SEID)
          programs_to_courses[program.name] = courses
      return(divisions_to_programs,programs_to_courses)
      ''' @return (divisions_to_programs, programs_to_courses) {tuple of dicts}
      1)division... @key = divisionName {string} @value = Programs{peewee obj}
      2)programs... @key = programName  {string} @value = Courses{peewee obj}''' 