from allImports import *
from app.users import get_user


@app.route("/courses", methods = ["GET"])

def courses():
    '''This function will render the correct template based off of the user's role'''
    user_name   = 'heggens'
    print user_name
    #user_info   = get_user(user_name)
    user_info   = Users.select().get()
    #print user_info.userName
    print str(user_info)
    return render_template("courses.html",
                            user_info = user_info,
                            cfg       = cfg)