from allImports import *
from app.users  import *
from app.switch import switch
import os

@app.route("/courses/", defaults={'post_CID': 0}, methods = ["GET", "POST"])
@app.route("/courses/<post_CID>", methods = ["GET", "POST"])
def courses(post_CID):
    '''This function will render the correct template based off of the user's role'''
    ERROR = 0
    #TYPE OF ERROR VALUES AND MEANINGS THAT COULD OCCUR ON THIS PAGE
    #ERROR = 0 NO ERROR OCCURED
    #ERROR = 1 COULD NOT AUTHENTICATE USER
    #ERROR = 2 AN ERROR OCCURED WHILE UPLOADING A FILE
    
    #WE WILL TO INTEGRATE LDAP AND GRAB THE INFORMATION FROM THAT
    user_name                 = 'heggens'   #Admin Access
    #user_name                 = 'pearcej'   #Division Chair Access
    #user_name                 = 'nakazawam' #Program Chair Access
    #user_name                 = 'jadudm'    #Faculty Access
    
    #GRAB THE USER'S INFORMATION
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
                                        .where(
                                                Divisions.DID == Divisions.DID
                                              ))
    for division in divisions:
        programs              = (Programs
                                        .select()
                                        .where(
                                                Programs.DID == division.DID
                                              ))
        divisions_to_programs[division.name] = programs
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
          programs_to_courses[program.name] = courses
    #SET THE DEFAULT DICTIONARY KEYS
    admin_key                   = None
    division_key                = None
    program_key                 = None
    my_courses_key              = None
    # MY COURSES SELECT QUERY
    my_courses                  = (UsersCourses
                                              .select()
                                              .join(Courses)
                                              .where(
                                                      UsersCourses.userName  == user_name,
                                                      UsersCourses.CID       == Courses.CID,
                                                      currentSEID[0].SEID    == Courses.SEID
                                                    ))
    #CHECK TO SEE IF THE USER HAS A MY COURSES TABLE
    try:
      temp_courses               = my_courses.get() #EXECUTE THE QUERY
    except:
      temp_courses               = None  
    if temp_courses != None:
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
                                          )).get()
        division_key            = division.name
        break;
      if case('program'):
        program                 = (Programs
                                          .select()
                                          .where(
                                                  Programs.PID == user_info.PID
                                                )).get()
        program_key             = program.name
        break;
        
      if case('faculty'):
        pass
        break;
      if case(): #THE DEFAULT IS TO ERROR OUT IF THE USERLEVEL IS NOT ONE OF THESE
        ERROR = 1
      ###############################################
      #THE CODE BELOW HANDLES ALL OF THE FILE UPLOAD#
      ###############################################
    if request.method     == "POST":
      app.logger.info("{0} attempting to upload file.".format(user_name))
      file = request.files['file']
      if ERROR == 0:
        try:
          #RETRIEVE THE COURSE INFORMATION FROM THE post_CID
          course_info         = (Courses
                                      .select()
                                      .join(Programs)
                                      .join(Divisions)
                                      .where(
                                              Courses.CID  == post_CID,
                                              Courses.PID  == Programs.PID,
                                              Programs.DID == Divisions.DID
                                            )).get()

          #SET THE FILE PATH FOR THE UPLOAD FOLDER
          upload_file_path       = cfg['fileOperations']['dataPaths']['uploads']
          course_file_path       = (    "/" 
                                      +  str(course_info.SEID.SEID) 
                                      + "/" 
                                      + str(course_info.PID.DID.name) 
                                      + "/" 
                                      + str(course_info.prefix) 
                                      + "/"
                                    ).replace(" ","")
          directory_paths = upload_file_path+course_file_path
          if not os.path.exists(directory_paths):
            os.makedirs(directory_paths)
          
          new_file_name          = (    'CID' 
                                      + str(course_info.CID) 
                                      + '-' 
                                      + str(course_info.prefix) 
                                      +  '-' 
                                      + str(course_info.number) 
                                      + '-' 
                                      + str(course_info.PID.DID.name) 
                                      + '-' 
                                      + user_name 
                                      + "." 
                                      + str(file.filename.split(".").pop())
                                    )
                                    
          complete_path          = (   directory_paths
                                      + new_file_name
                                    ).replace(" ", "")
          file.save(complete_path)
        except:
         
          sys.exc_info()[0]
          ERROR = 2
          
        update_course = Courses.update(filePath=complete_path).where(Courses.CID==post_CID)
        update_course.execute()
          
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