from allImports import *
from app.users  import *
from app.switch import switch

@app.route("/courses", methods = ["GET"])

def courses():
    '''This function will render the correct template based off of the user's role'''
    user_name         = 'heggens' #We will eventually need to get this through LDAP
    user_info         = get_user(user_name)
    my_courses        = (UsersCourses
                                      .select()
                                      .where(
                                              UsersCourses.userName == user_name
                                              ))
    user_level        = check_user_level(user_name)      
    #Render The correct template based off the users level
    if user_level == "error":
      message = "There was an error during the authentication process."
      return render_template("error.html",
                              cfg = cfg,
                              message = message
                            )
    for case in switch(user_name):
      if case('admin'):
        #Find the courses the administrator can use
        break;
      if case('division_chiar'):
        #Find the program_chair courses
        break;
      if case('program_chair'):
        #Find the division_chair courses
        break;
      if case('faculty'):
        #use the mycourses