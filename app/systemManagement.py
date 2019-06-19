from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url
from app.logic.getSystemManagement import GetSystemManagement
from app.logic import databaseInterface

@app.route("/admin/systemManagement", methods=["GET", "POST"])
def systemManagement():
  page = "/" + request.url.split("/")[-1] #We need page for logging purposes
  authorizedUser = AuthorizedUser()
  if authorizedUser.isAdmin:              #Ensure that the user is an Admin
    #Class from logic folder
    system    = GetSystemManagement()
    years     = system.get_years_list()   #Returns a list of the next five years
    #DatabaseInterface from logic folder
    semesters = databaseInterface.get_all_semesters()
    users     = databaseInterface.get_non_admins()
    admins    = databaseInterface.get_all_admins()
    return render_template('admin/editSystem.html',
                            cfg = cfg,
                            #This variable is for the navbar
                            isAdmin   = authorizedUser.isAdmin,
                            users     = users,
                            admins    = admins,
                            semesters = semesters,
                            years     = years,
                            )
  else:
    abort(403)
                            
@app.route("/admin/systemManagement/add", methods=["POST","GET"])
def addSemester():
  page = "/" + request.url.split("/")[-1]
  authorizedUser = AuthorizedUser()
  if authorizedUser.isAdmin:
    data        = request.form
    #Class from logic folder
    system      = GetSystemManagement()
    logList     = system.add_semester(data)
    print logList
    #TODO: figure out how to log
    log.writer(logList[0],page,logList[1])
    flash(logList[1])
    return redirect(redirect_url())
  else:
    abort(403)
      
                            