from app.allImports import *

class AuthorizedUser:
  def __init__(self):
    #self.username = authUser(request.environ)
    self.username = 'heggens'

  def get_username(self):
    return self.username
  
  def get_user(self):
      user = Users.get(Users.username == self.username)
      return user
    
  def user_level(self):
      #user = get_user(user_name)
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
                        
