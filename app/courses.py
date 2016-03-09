from allImports import *
from app import getUserData


@app.route("/courses", methods = ["GET"])

def courses():
    '''This function will render the correct template based off of the user's role'''
    un = "heggens"
    UID = getUID(un)
    RID = getRID(un)
    return render_template("courses.html",
                            cfg = cfg)