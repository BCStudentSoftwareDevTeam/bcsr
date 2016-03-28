from allImports import *
from app.users  import *
from app.switch import switch

@app.route("/courses", methods = ["GET"])

def courses():
    '''This function will render the correct template based off of the user's role'''
    #GRAB THE USER'S INFORMATION
    user_name                 = 'heggens' #WE WILL TO INTEGRATE LDAP AND GRAB THE INFORMATION FROM THAT
    user_level                = check_user_level(user_name)
    user_info                 = get_user(user_name)
    #RETRIEVE THE CURRENT SEMESTER
    currentSEID               = (Semesters.select()
                                            .where(
                                                    Semesters.current == True
                                                  ))
   #CREATE TWO DEFAULT DICTIONARIES
    divisions_to_programs     = {} #CONTAINS THE MAPPING OF ALL DIVISIONS TO PROGRAMS
    programs_to_courses       = {} #CONTAINS ALL THE MAPPING OF CURRENT SEMESTER COURSES TO PROGRAMS
    divisions                 = (Divisions 
                                        .select()
                                        .order_by(+Divisions.DID)
                                )
    for division in divisions:
        programs              = (Programs
                                        .select()
                                        .where(
                                                Programs.DID == division.DID
                                              ))
        divisions_to_programs[division] = programs
        for program in programs:
          #NOTE: NEED TO IMPLEMENT QUERY FROM USERSCOURSES SO THAT WE CAN ACCESS THE USER'S INFORMATION
          courses               = (UsersCourses
                                                .select()
                                                .join(Courses)
                                                .order_by(+Courses.prefix)
                                                .where(
                                                        UsersCourses.CID  == Courses.CID,
                                                        Courses.PID       == program.PID,
                                                        Courses.SEID      == currentSEID[0].SEID
                                                      ))
          programs_to_courses[program] = courses 
    #SET THE DEFAULT DICTIONARY KEYS
    admin_key                   = None
    division_key                = None
    program_key                 = None
    my_courses_key              = None
    #RETRIEVE THE USERS COURSE INFORMATION
    my_courses                  = (UsersCourses
                                              .select()
                                              .join(Courses)
                                              .where(
                                                      UsersCourses.userName  == user_name,
                                                      UsersCourses.CID       == Courses.CID,
                                                      currentSEID[0].SEID    == Courses.SEID
                                                    ))
    #TODO: CHECK TO SEE IF THE MY_COURSES VARIABLE HAD ANYTHING RETURNED
    #IF IT DID THEN WE NEED TO SET THE my_courses_key = True                                              
    my_courses_key = True
    #SET THE DICTIONARY KEYS IF THE USER HAS THE CORRECT ACCESS LEVEL
    for case in switch(user_level):
      if case('admin'):
        admin_key = True              
        break;
      if case('division'):
        division                = (Divisions
                                          .select()
                                          .where(
                                                  Divisions.DID == user_info.DID
                                          ))
        division_key            = division
        break;
      if case('program'):
        program                 = (Programs
                                          .select()
                                          .where(
                                                  Programs.PID == user_info.PID
                                                ))
        program_key             = program
        break;
        
      if case('faculty'):
        pass
        break;
      if case(): #THE DEFAULT IS TO ERROR OUT IF THE USERLEVEL IS NOT ONE OF THESE
        message        = "There was an error during the authentication process."
        return render_template("error.html",
                                cfg     = cfg,
                                message = message
                              )
                                
    return render_template("courses.html",
                            cfg                     = cfg,
                            divisions_to_programs   = divisions_to_programs,
                            programs_to_courses     = programs_to_courses,
                            my_courses              = my_courses,
                            my_courses_key          = my_courses_key,
                            program_key             = program_key,
                            division_key            = division_key,
                            admin_key               = admin_key
                            )