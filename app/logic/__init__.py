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
                                        
def grab_courses_in_program(PID,SEID):
    peeweeObj               = (UsersCourses
                                          .select()
                                          .join(Courses)
                                          .order_by(+UsersCourses.username, +Courses.prefix, +Courses.number)
                                          .where(
                                                  UsersCourses.CID  == Courses.CID,
                                                  Courses.PID       == PID,
                                                  Courses.SEID      == SEID
                                                ))
    return peeweeObj
    
def grab_my_courses(username,SEID):
  my_courses = (UsersCourses
                            .select()                      
                            .join(Courses)
                            .where(
                                    UsersCourses.username  == username,
                                    UsersCourses.CID       == Courses.CID,
                                    Courses.SEID           == SEID
                                   ))
  if my_courses.exists(): #checking whether query contains courses
    peeweeObj = my_courses.execute()
    return peeweeObj
  else:
    return None

def get_all_semesters():
  semesters = Semesters.select()
  return semesters
  
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

def get_course_download_file_path(CID):
  course = get_course_info(CID)
  file_path = str(cfg['fileOperations']['dataPaths']['download']) + str(course.filePath)
  return file_path
 
def get_course_instructors(CID):
  instructors_string = ''
  instructors = UsersCourses.select().where(UsersCourses.CID == CID)
  for instructor in instructors:
    print instructor.username.username
    instructors_string += instructor.username.username
  return instructors_string
  
def get_non_admins():
  users = Users.select().where(Users.isAdmin == 0)
  return users
  
def get_all_admins():
  admins = Users.select().where(Users.isAdmin == 1)
  return admins
  
def check_strings(strings):
  for string in strings:
    if string != '' or string != None:
      result = isinstance(string,str)
      if result == False:
        return False
    else:
      return False
  return True
  
def check_integers(integers):
  for integer in integers:
    result = isinstance(integer,int)
    if result == False:
      return False
  return True
  
def insert_course(pre,num,sect,pid,seid):
  try:
    string_result  = check_strings([pre,num,sect])   
    integer_result = check_integers([pid,seid])
    if string_result == True and integer_result == True:
      new_course = Courses(prefix=pre,number=num,section=sect,PID=pid,SEID=seid)
      new_course.save()
    else:
      return False
    return new_course
  except Exception as e:
    return False
    
def insert_course_user(un,cid):
  try:
    newInsert = UsersCourses(username=un,CID=cid)
    newInsert.save()
    if newInsert:
      return newInsert
    else:
      return False
  except Exception as e:
    return False
