from allImports import *
import sys

def get_user(user_name):
    user = (Users
                  .select()
                  .where(
                            Users.userName == user_name
                        ))
    return user
    
def check_user_level(user_name):
    #user = get_user(user_name)
    user = (Users
                  .select()
                  .where(
                            Users.userName == user_name
                        ))
    try:
        if user.admin:
            return 'admin'
        else:
            return 'failed'
    except:
        pass
                        
