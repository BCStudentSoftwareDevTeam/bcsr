from allImports import *
#IMPORT LOGIC FILES
from app.logic import databaseInterface
from app.logic.getAuthUser import AuthorizedUser 
from app.logic.getCourses import GetCourses
from app.logic.switch import switch

@app.route("/courses", methods = ["GET"]) #SET A DEFAULT APP ROUTE

def courses():
    '''This function will render the correct template based off of the user's role'''
    # Grab: (user_name,user_level,user_info)
    auth       = AuthorizedUser()
    user       = auth.get_user()
    user_level = auth.user_level()
    
    
    #CREATE TWO DEFAULT DICTIONARIES
    getCourses            = GetCourses()
    two_dictionaries = getCourses.create_dictionaries()
    divisions_to_programs = two_dictionaries[0]
    programs_to_courses   = two_dictionaries[1]
    # MY COURSES SELECT QUERY
    my_courses                  = getCourses.check_for_my_courses()
    # RENDER CORRECT PAGE BASED ON ACCESS LEVEL
    for case in switch(user_level):
      if case('admin'):
        return render_template('courses/admin.html',
                                cfg                   = cfg,
                                my_courses            = my_courses,
                                divisions_to_programs = divisions_to_programs,
                                programs_to_courses   = programs_to_courses
                               )              
        break;
      if case('division'):
        division                = databaseInterface.get_division(user.isDivision)
        division_key            = division.name
        return render_template('courses/division.html',
                                cfg                   = cfg,
                                my_courses            = my_courses,
                                division_key          = division_key,
                                divisions_to_programs = divisions_to_programs,
                                programs_to_courses   = programs_to_courses
                               )   
        break;
      if case('program'):
        program                 = databaseInterface.get_program(user.isProgram)
        program_key             = program.name
        return render_template('courses/program.html',
                                cfg                   = cfg,
                                my_courses            = my_courses,
                                _key                  = program_key,
                                programs_to_courses   = programs_to_courses
                               )    
        break;
        
      if case('faculty'):
        return render_template('courses/faculty.html',
                                cfg                   = cfg,
                                my_courses            = my_courses
                               )  
        break;
      if case(): 
        # TODO: return ERROR
        render_template('error.html')
        
