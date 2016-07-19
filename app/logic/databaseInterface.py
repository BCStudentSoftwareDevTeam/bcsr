from app.allImports import *

def grab_current_semester():
    semesters = Semesters.select()
    current = 0
    for semester in semesters:
      if semester.SEID > current:
        current = semester.SEID
    return current

def grab_all_divisions():
    peeweeObj = Divisions.select().order_by(+Divisions.DID)
    return peeweeObj
    
def grab_programs_in_division(DID):
  peeweeObj = (Programs.select().where(Programs.DID == DID))
  return peeweeObj
                                        
def grab_courses_in_program(PID):
    peeweeObj               = (UsersCourses
                                          .select()
                                          .join(Courses)
                                          .order_by(+Courses.prefix)
                                          .where(
                                                  UsersCourses.CID  == Courses.CID,
                                                  Courses.PID       == PID,
                                                  Courses.SEID      == grab_current_semester()
                                                ))
    return peeweeObj
    
def grab_my_courses(username):
  my_courses = (UsersCourses
                            .select()                      
                            .join(Courses)
                            .where(
                                    UsersCourses.username  == username,
                                    UsersCourses.CID       == Courses.CID,
                                    Courses.SEID      == grab_current_semester()
                                   ))
  peeweeObj = my_courses.execute()
  return peeweeObj
  
def get_division(DID):
  division = Divisions.get(Divisions.DID == DID)
  return division
  
def get_program(PID):
  program = Programs.get(Programs.PID == PID)
  return program
  
def get_course_info(CID):
  course = (Courses
                    .select()
                    .join(Programs)
                    .join(Divisions)
                    .where(
                            Courses.CID  == CID,
                            Courses.PID  == Programs.PID,
                            Programs.DID == Divisions.DID
                          )).get()
  return course
  
def get_course_file_path(CID):
  course = get_course_info(CID)
  file_path = str(cfg['fileOperations']['dataPaths']['uploads']) + str(course.filePath)
  return file_path
  
      
                                          
    
    