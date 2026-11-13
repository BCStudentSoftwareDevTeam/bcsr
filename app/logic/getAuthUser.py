'''Any function that is related to user information or authentication should
be located here'''
from app.allImports import *
from app.models import *

class AuthorizedUser:
  def __init__(self):
    self.username  = authUser(request.environ)
    self.isStudent = self.is_student()
    if self.isStudent:
      self.isAdmin = False
    else:
      self.isAdmin = self.get_user().isAdmin

  def get_username(self):
    '''returns the username of the user'''
    return self.username

  def get_user(self):
    '''retruns the user object corresponding to the logged on user'''
    user = Users.get_or_none(Users.username == self.username)
    if user:
      return user
    else:
      abort(403)

  def is_student(self):
    '''students are not in Users, so Shibboleth's description is how we know them'''
    if self.username is None or "student" not in authDescription(request.environ):
      return False
    return Users.get_or_none(Users.username == self.username) is None

  def user_level(self):
    # students have no Users row, so they are checked before get_user()
    if self.isStudent:
      return 'student'
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
