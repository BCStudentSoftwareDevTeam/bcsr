from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url

@app.route('/editAdmin/<action>', methods=["POST"])
def editAdmin(action):
  authorizedUser = AuthorizedUser()
  if authorizedUser.isAdmin:
    
    if action == 'add':
      #message = "User: ( " + username + " ) has been added as an Admin."
      message = "User: ( Test Message ) has been added as an Admin."
    elif action == 'remove':
      message = "User: ( Test Message ) has been removed as an Admin."
    else:
      message = 'An error occured while trying to edit data.' 
      #TODO: LOG HERE
    flash(message)
    return redirect(redirect_url('systemManagement'))
  else:
    abort(403)