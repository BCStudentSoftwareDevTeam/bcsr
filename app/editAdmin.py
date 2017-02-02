from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url

@app.route('/editAdmin/<action>', methods=["POST"])
def editAdmin(action):
  authorizedUser = AuthorizedUser()
  if authorizedUser.isAdmin:
    if action == 'add':
      user = request.form.getlist('users[]')
      print user
      if user:
        message = "User: ( " + user + " ) has been added as an Admin."
      else:
        message = "user is not passing the test"
    elif action == 'remove':
      message = "User: ( Test Message ) has been removed as an Admin."
    else:
      message = 'An error occured while trying to edit data.' 
      #TODO: LOG HERE
    flash(message)
    return redirect(redirect_url('systemManagement'))
  else:
    abort(403)