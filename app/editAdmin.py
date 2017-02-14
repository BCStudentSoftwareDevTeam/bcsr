from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url

@app.route('/editAdmin', methods=["POST"])
def editAdmin():
  try:
    username = authUser(request.environ)
    authorizedUser = AuthorizedUser()
    if authorizedUser.isAdmin:
      data = request.form
      if data['admin[]'] != "" and data['admin'] is not None: 
        user = Users.get(Users.username == data['admin[]'])
        print user.isAdmin
        if user.isAdmin:
          message = "User: ({}) has been removed as an Admin.".format(user.username)
        else:
          message = "User: ({}) has been added as an Admin.".format(user.username)
        #flip the boolean
        user.isAdmin = not user.isAdmin
        user.save()
        #TODO: LOG HERE
        flash(message)
        return redirect(redirect_url('systemManagement'))
      else:
        flash("No user was selected.")
        return redirect(redirect_url('systemManagement'))
    else:
      abort(403)
  except Exception as e:
    #TODO: Log Message
    message = "An error occured while processing data"
    flash(e)
    return redirect(redirect_url('systemManagement'))

  