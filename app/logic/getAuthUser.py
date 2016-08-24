'''Any function that is related to user information or authentication should
be located here'''
from app.allImports import *

class AuthorizedUser:
  def __init__(self):
    self.username = authUser(request.environ)
    self.isAdmin  = self.get_user().isAdmin 

  def get_username(self):
    '''returns the username of the user'''
    return self.username
  
  def get_user(self):
    '''retruns the user object corresponding to the logged on user'''
    user = Users.select().where(Users.username == self.username)
    if user:
      return user
    else:
      return 0
    
  def user_level(self):
    user = self.get_user()
    try:
        if user.isAdmin:
            return 'admin'
        elif user.PID is not None:
            return 'program'
        elif user.DID is not None:
            return 'division'
        else:
            return 'faculty'
        except:
            return "error"

