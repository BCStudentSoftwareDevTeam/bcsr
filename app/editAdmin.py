from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url

def checkData(data,key):
  user    = None
  message = None
  try:
    if data[key] != "" and data[key] is not None:
      user = Users.get(Users.username == data[key])
      if user.isAdmin:
        message = "User: ({}) has been removed as an Admin.".format(user.username)
      else:
        message = "User: ({}) has been added as an Admin.".format(user.username)
    else:
      message="No user was selected."
  except Exception as e:
    message = "Either a bad key or username is not in database."
  return [user, message]

@app.route('/admin/userManagement/changeAdministrator', methods=["POST"])
def editAdmin():
  username = authUser(request.environ)
  authorizedUser = AuthorizedUser()
  if authorizedUser.isAdmin:
    data    = request.form
    key     = 'admin[]'
    result  = checkData(data,key)
    user    = result[0]
    if user is not None:
      user.isAdmin = not user.isAdmin #Flip the boolean value
      user.save()
      #TODO: LOG HERE
    flash(result[1])
    return redirect(redirect_url('userManagement'))
  else:
    abort(403)
