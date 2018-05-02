from allImports import *
#IMPORT LOGIC FILES
from app.logic import databaseInterface
from app.logic.getAuthUser import AuthorizedUser 
from app.logic.getCourses import GetCourses
from app.logic.switch import switch
from app.logic.getAll import GetAll

@app.route("/courses", methods = ["GET"]) #SET A DEFAULT APP ROUTE

def courses():
    '''This function will render the correct template based off of the user's role'''
    #activate classes used on this controller
    getAll                = GetAll()
    #Grab user information
    auth       = AuthorizedUser()
    user       = auth.get_user()
    user_level = auth.user_level()
    #CREATE TWO DEFAULT DICTIONARIES
    currentSEID           = databaseInterface.grab_current_semester()
    current_term          = Semesters.get(Semesters.SEID == currentSEID)
    getCourses            = GetCourses(auth)
    # we need to get the dictionaries that populate the tables
    two_dictionaries      = getAll.create_dictionaries(currentSEID)
    divisions_to_programs = two_dictionaries[0]
    programs_to_courses   = two_dictionaries[1]
    # MY COURSES SELECT QUERY
    my_courses                  = getCourses.check_for_my_courses(currentSEID)
    CID = list()
    for course in my_courses:
        cid = course.CID
        if cid not in CID:
            CID.append(cid)

    courses_with_files = FilesCourses.select().join(Courses).where(Courses.CID << CID)
    courses_to_files = dict()
    for course in courses_with_files:
        if course.CID in courses_to_files:
            courses_to_files[course.CID].append(course.FID)
        else:
            courses_to_files[course.CID] = [course.FID]
    # syllabus_dict = {}
    # for course in my_courses:
    #     syllabus_dict[course.CID] = ((course.filePath).split()).pop()
    # print(syllabus_dict)                
    print (my_courses)
    semesters = databaseInterface.get_all_semesters()
    # RENDER CORRECT PAGE BASED ON ACCESS LEVEL
    return render_template('courses/admin.html',
                                cfg                   = cfg,
                                my_courses            = my_courses,
                                isAdmin               = auth.isAdmin,
                                divisions_to_programs = divisions_to_programs,
                                programs_to_courses   = programs_to_courses,
                                semesters             = semesters,
                                current_term          = current_term,
                                courses_to_files      = courses_to_files 
                               )
                               
    @app.route("/courses/files/<CID>", methods = ["GET"])
    def redirectToDelete(CID):
        #activate classes used on this controller
        getAll                = GetAll()
        #Grab user information
        auth       = AuthorizedUser()
        user       = auth.get_user()
        user_level = auth.user_level()
    
    return render_template('courses/admin.html',
                                cfg                   = cfg,
                                my_courses            = my_courses,
                                isAdmin               = auth.isAdmin,
                                divisions_to_programs = divisions_to_programs,
                                programs_to_courses   = programs_to_courses,
                                semesters             = semesters,
                                current_term          = current_term
                               )
        
    # TO-DO:
        # Implement level of access for users; hence the reason the bottom lines were commented out/ 
       
    
    

    
    # for case in switch(user_level):
    #   if case('admin'):
    #     return render_template('courses/admin.html',
    #                             cfg                   = cfg,
    #                             my_courses            = my_courses,
    #                             isAdmin               = auth.isAdmin,
    #                             divisions_to_programs = divisions_to_programs,
    #                             programs_to_courses   = programs_to_courses,
    #                             semesters             = semesters,
    #                             current_term          = current_term
    #                           )              
    #     break;
    #   if case('division'):
    #     division_key            = user.DID
    #     print division_key
    #     return render_template('courses/division.html',
    #                             cfg                   = cfg,
    #                             my_courses            = my_courses,
    #                             division_key          = division_key,
    #                             divisions_to_programs = divisions_to_programs,
    #                             programs_to_courses   = programs_to_courses,
    #                             current_term          = current_term
    #                           )   
    #     break;
    #   if case('program'):
    #     program_key             = user.PID.name
    #     return render_template('courses/program.html',
    #                             cfg                   = cfg,
    #                             my_courses            = my_courses,
    #                             program_key           = program_key,
    #                             programs_to_courses   = programs_to_courses,
    #                             current_term          = current_term
    #                           )    
    #     break;
        
    #   if case('faculty'):
    #     return render_template('courses/faculty.html',
    #                             cfg                   = cfg,
    #                             my_courses            = my_courses,
    #                             current_term          = current_term
    #                           )  
    #     break;
    #   if case(): 
    #     # TODO: return ERROR
    #     abort(404)
    #     render_template('error.html')
        

