from allImports import *
from app.users  import get_user
from app.switch import switch

@app.route("/courses", methods = ["GET"])

def courses():
    '''This function will render the correct template based off of the user's role'''
    user_name         = 'heggens' #We will eventually need to get this through LDAP
    user_info         = get_user(user_name)
    



















































