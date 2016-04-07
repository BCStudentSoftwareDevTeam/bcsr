from allImports import *
import sys

def get_user(user_name):
    user = (Users
                  .select()
                  .where(
                            Users.userName == user_name
                        )).get()
    return user
    
def check_user_level(user_name):
    #user = get_user(user_name)
    user = (Users
                  .select()
                  .where(
                            Users.userName == user_name
                        ).get())
    try:
        if user.admin:
            return 'admin'
        elif user.PID is not None:
            return 'program'
        elif user.DID is not None:
            return 'division'
        else:
            return 'faculty'
    except:
        return "error"
                        
