'''Any function that is related to user information or authentication should
be located here'''
from app.allImports import *
from app.models import *

class AuthorizedUser:
  def __init__(self):
    self.username  = authUser(request.environ)
    self.user      = Users.get_or_none(Users.username == self.username)
    # students are not in Users, Shibboleth's description tells us they are students
    self.isStudent = self.user is None and bool(self.username) and "student" in authDescription(request.environ)
    if self.user is None and not self.isStudent:
      abort(403)
    self.isAdmin   = bool(self.user and self.user.isAdmin)

  def get_username(self):
    '''returns the username of the user'''
    return self.username

  def get_user(self):
    '''retruns the user object corresponding to the logged on user'''
    if self.user:
      return self.user
    else:
      abort(403)

  def user_level(self):
    user = self.user
    try:
      # checked first because every other level needs a Users row
      if self.isStudent:
        return 'student'
      elif user.isAdmin:
        return 'admin'
      elif user.PID is not None:
        return 'program'
      elif user.DID is not None:
        return 'division'
      else:
        return 'faculty'
    except:
      return "error"
