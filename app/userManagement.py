from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url
from app.logic.getSemesterManagement import GetSemesterManagement
from app.logic import databaseInterface

@app.route("/admin/userManagement", methods=["GET", "POST"])
def userManagement():
  page = "/" + request.url.split("/")[-1] #We need page for logging purposes
  authorizedUser = AuthorizedUser()
  if authorizedUser.isAdmin:              #Ensure that the user is an Admin
    #Class from logic folder
    semester    = GetSemesterManagement()

    #DatabaseInterface from logic folder
    semesters = databaseInterface.get_all_semesters()
    users     = databaseInterface.get_non_admins()
    admins    = databaseInterface.get_all_admins()
    return render_template('admin/userManagement.html',
                            cfg = cfg,
                            #This variable is for the navbar
                            isAdmin   = authorizedUser.isAdmin,
                            users     = users,
                            admins    = admins,
                            )
  else:
    abort(403)
