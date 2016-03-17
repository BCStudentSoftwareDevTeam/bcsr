from allImports import *
from app.users  import *
from app.switch import switch

@app.route("/courses", methods = ["GET"])

def courses():
    '''This function will render the correct template based off of the user's role'''
    user_name         = 'heggens' #We will eventually need to get this through LDAP
    user_info         = get_user(user_name)
    my_courses        =  (UsersCourses
                                        .select()
                                        .where(
                                                UsersCourses.userName == user_name
                                                ))
                                                
    return render_template("courses.html",
                            cfg = cfg,
                            user_info = user_info)
                            
    