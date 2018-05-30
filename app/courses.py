from allImports import *
#IMPORT LOGIC FILES
from app.logic import databaseInterface
from app.logic.getAuthUser import AuthorizedUser 
from app.logic.getCourses import GetCourses
from app.logic.switch import switch
from app.logic.getAll import GetAll

@app.route("/courses", methods = ["GET"], defaults ={'SEID':None, 'filterType':None}) #SET A DEFAULT APP ROUTE
@app.route("/courses/<SEID>", methods=["GET"], defaults ={'filterType':None})
@app.route("/courses/<SEID>/<filterType>", methods=["GET"])
def courses(SEID, filterType):
    '''This function will render the correct template based off of the user's role'''
    #activate classes used on this controller
    getAll                = GetAll()
    #Grab user information
    auth       = AuthorizedUser()
    user       = auth.get_user()
    user_level = auth.user_level()
    #CREATE TWO DEFAULT DICTIONARIES
  
    if SEID is None:
        currentSEID           = databaseInterface.grab_current_semester()
        current_term          = Semesters.get(Semesters.SEID == currentSEID)
    else:
        currentSEID = SEID
        current_term = Semesters.get(Semesters.SEID == currentSEID)
    getCourses            = GetCourses(auth)
    
    # we need to get the dictionaries that populate the tables
    two_dictionaries      = getAll.create_dictionaries(currentSEID)
    divisions_to_programs = two_dictionaries[0]
    programs_to_courses   = two_dictionaries[1]
    # MY COURSES SELECT QUERY
<<<<<<< HEAD
    if filterType == "allCourses" or filterType == None:
        my_courses = getCourses.check_for_my_courses(currentSEID)
    
    if filterType == "withSyllabus":
        my_courses = getCourses.check_for_my_courses_with_syllabus(currentSEID)

    if filterType == "noSyllabus":
        my_courses = getCourses.check_for_my_courses_with_no_syllabus(currentSEID)
   
    syllabus_dict = {}
    additional_dict = {}
    print (currentSEID)
    if my_courses is not None: 
        for course in my_courses:
            if course.CID.filePath is not None:
                syllabus_dict[course.CID.CID] = (course.CID.filePath.split("/")).pop()
            if course.CID.optionalFilepath is not None:
                additional_dict[course.CID.CID] = (course.CID.optionalFilepath.split("/")).pop()
            
            
            

    #To-Do: create additional file dictionary for the view
    
=======
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
>>>>>>> b01e646186df1c4785d24ce459fc415d078eac5a
    semesters = databaseInterface.get_all_semesters()
    # RENDER CORRECT PAGE BASED ON ACCESS LEVEL
    return render_template('courses/admin.html',
                                cfg                   = cfg,
                                syllabus_dict         = syllabus_dict,
                                additional_dict       = additional_dict,
                                my_courses            = my_courses,
                                isAdmin               = auth.isAdmin,
                                divisions_to_programs = divisions_to_programs,
                                programs_to_courses   = programs_to_courses,
                                semesters             = semesters,
                                current_term          = current_term,
<<<<<<< HEAD
                                currentSEID          = currentSEID
                                
=======
                                courses_to_files      = courses_to_files 
>>>>>>> b01e646186df1c4785d24ce459fc415d078eac5a
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
        

