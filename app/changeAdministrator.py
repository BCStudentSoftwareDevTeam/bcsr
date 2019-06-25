from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url
from app.logic.getSemesterManagement import GetSemesterManagement
from app.logic import databaseInterface
from app.programManagement import adminProgramManagement

@app.route("/admin/userManagement/changeAdministrator", methods=["GET", "POST"])
def changeAdministrator():
  page = "/" + request.url.split("/")[-1] #We need page for logging purposes
  authorizedUser = AuthorizedUser()
  if authorizedUser.isAdmin:              #Ensure that the user is an Admin
    if request.method == "GET":

        users     = databaseInterface.get_non_admins()
        admins    = databaseInterface.get_all_admins()

        return render_template('admin/userManagement/changeAdministrator.html',
                                cfg = cfg,
                                isAdmin   = authorizedUser.isAdmin,
                                users     = users,
                                admins    = admins
                                )
  else:
    abort(403)
