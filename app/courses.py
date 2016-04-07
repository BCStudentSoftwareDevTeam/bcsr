from allImports import *
from app.users  import *
from app.switch import switch
import os

@app.route("/courses/", defaults={'post_CID': 0}, methods = ["GET", "POST"])
@app.route("/courses/<post_CID>", methods = ["GET", "POST"])
def courses(post_CID):
    '''This function will render the correct template based off of the user's role'''
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
                                              )
)
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
        message        = "There was an error during the authentication process."
        return render_template("error.html",
                                cfg     = cfg,
                                message = message
                              )
      ###################################################
      #THE CODE BELOW HANDLES ALL OF THE FILE MANAGEMENT#
      ###################################################
      #TODO: ALLOWED_EXTENTIONS AND AND UPLOAD FOLDER ARE NOW LOCATED INSIDE OF THE CONFIG.YAML FOLDER 
      #TODO: FIX THE CODE BELOW TO REFLECT THE CHANGES
      if request.method     == "POST":
        #TODO: CHECK TO SEE IF THEY ARE AN AUTHORIZED USER
        app.logger.info("{0} attempting to upload file.".format(user_name))
        #RETRIEVE THE COURSE INFORMATION FROM THE post_CID
        course_info         = (Courses
                                    .select()
                                    .join(Programs)
                                    .where(
                                            Courses.CID == post_CID,
                                            Courses.PID == Programs.PID
                                          )).get()
        #SET THE FILE PATH FOR THE UPLOAD FOLDER
        UPLOAD_FOLDER       = #MOVED TO THE YAML
        #THE REST OF THE PATH INFOMATION --> str(Courses.SEID) + "/" + str(Courses.PID.DID.name) + "/" + str(Courses.prefix) + "/"
        UPLOAD_FOLDER       = UPLOAD_FOLDER.replace(" ", "") #MAKE SURE THAT THE FILE PATH DOES NOT CONTAIN ANY WHITE SPACES
        #CHECK TO SEE IF THE FILE IS PART OF OUR ALLOWED_EXTENTIONS
        ALLOWED_EXTENTIONS  = 
        def allowed_file(filename):
          return '.' in filename and \
            filename.rsplit('.',1)[1] in ALLOWED_EXTENTIONS
        #TODO: CHECK THE FILE SIZE
        #START HANDLING THE FILE    
        file                = request.files['file']
        if file and allowed_file(file.filename):
          filename = 'CID' + str(Courses.CID) + '-' + str(Courses.prefix) +  '-' + str(Courses.number) + '-' + str(Courses.PID.DID.name) + '-' + user_name + "." + str(os.path.splitext(filename))[1]
          file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)
          #RENAME THE FILE TO OUR FILE NAMEING SYSTEM
        
    
        
      
        
        
        
        
        
        
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