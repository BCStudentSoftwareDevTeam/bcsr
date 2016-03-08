from allImports import *

@app.route("/courses", methods = ["GET"])

def courses():
    '''This function will render the correct template based off of the user's role'''
    