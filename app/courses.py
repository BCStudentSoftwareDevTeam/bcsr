from allImports import *
from app.users  import get_user
from app.switch import switch


@app.route("/courses", methods = ["GET"])

def courses():
    '''This function will render the correct template based off of the user's role'''
    user_name         = 'heggens'
    user_info         = get_user(user_name)
    
    current_semester  = (CurrentSemester
                          .select()
                          .where(CurrentSemester.CSEID == 1
                        )).get()
    current_SEID      = current_semester.SEID
    
    my_courses_query  = (UsersToSCS
                          .select()
                          .join(SyllabusCourseSemester)
                          .where(
                                  (UsersToSCS.UID               == user_info.UID) &
                                  (UsersToSCS.SCSID             == SyllabusCourseSemester.SCSID) &
                                  (SyllabusCourseSemester.SEID  == current_SEID) 
                                  
                                  
    )).execute()
    #TODO:CREATE MY COURSES TABLE
    
    for case in switch(user_info.RID.name):
      if case('Administrator'):
        divisionDictionary  = {}
        programDictionary   = {}
        divisions    = (Divisions
                            .select(
                          )).execute()
        for division in divisions:      
          programs   = (DivisionToProgram
                            .select()
                            .where(
                                    (DivisionToProgram.DID == division.DID)
                          )).execute()
          for program in programs:
            program_table = []   #this will hold all of the rows that will be in the program table
            program_dict_key        = (Programs
                                        .select(Programs.name)
                                        .where(
                                               (Programs.PID == program.PID)
                                      )).get()
            syllabusCourseSemester  = (SyllabusCourseSemester
                                      .select()
                                      .join(Courses)
                                      .where(
                                              (SyllabusCourseSemester.SEID  == current_SEID) &
                                              (SyllabusCourseSemester.CID   == Courses.CID)  &
                                              (Courses.PID                  == program.PID) 
                                      )).execute()
            for scs in syllabusCourseSemester:
              #start collecting the data that will be in the td
              table_row     = [] #Make sure the that the table row is empty
              instructor    = (Users
                              .select(Users.firstName,Users.lastName)
                              .join(UsersToSCS)
                              .where(
                                      (Users.UID        == UsersToSCS.UID) &
                                      (UsersToSCS.SCSID == scs.SCSID)
                              )).execute()
              #instructor_td = str(instructor.firstName) + ' ' + str(instructor.lastName)
              course        = (Courses
                              .select(Courses.prefix,Courses.number,Courses.section)
                              .join(SyllabusCourseSemester)
                              .where(
                                      (Courses.CID                   == SyllabusCourseSemester.CID) &
                                      (SyllabusCourseSemester.SCSID  == scs.SCSID)
                              )).execute()
              prefix_td     = course.prefix
              number_td     = course.number
              section_td    = course.section
              
              semester      = (Semester
                              .select(Semester.year,Semester.term)
                              .join(SyllabusCourseSemester)
                              .where(
                                      (SyllabusCourseSemester.SCSID  == scs.SCSID) &
                                      (Semester.SEID                 == SyllabusCourseSemester.SEID)
                            )).execute()
              year_td       = semester.year
              term_td       = semester.term
              
              table_row     = [instructor_td , prefix_td, number_td, section_td, year_td, term_td]
              program_table.append[table_row] # Now add the data to the program rows
            #######################################################################################
            #After we have collected all of the rows in the program table using the scsid
            #we create a dictionary that will link the program name to the matrix of all the table rows and columns
            programDictionary[program_dict_key] = program_rows                      
                                     
              
              
        #TODO: Create Administration View
        break
      if case('Division Chair'):
        #TODO: Create Program Chair View
         break
      if case('Program Chair'):
        #TODO: Create Division Chair View
        break
      if case('Professor'):
        #TODO: Create Professor View
        break
      if case():
        test = 'fail'
    return render_template("courses.html",
                            user_info = user_info,
                            cfg       = cfg)