from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url
from app.logic.getSystemManagement import GetSystemManagement

@app.route("/admin/systemManagement", methods=["GET", "POST"])
def systemManagement():
  page = "/" + request.url.split("/")[-1]
  authorizedUser = AuthorizedUser()
  if authorizedUser.isAdmin:
    system    = GetSystemManagement()
    semesters = Semesters.select()
    years     = system.get_years_list()
    return render_template('admin/editSystem.html',
                            cfg = cfg,
                            #This variable is for the navbar
                            isAdmin       = authorizedUser.isAdmin,
                            semesters = semesters,
                            years     = years,
                            )
                            
@app.route("/admin/systemManagement/add", methods=["POST","GET"])
def addSemester():
  page = "/" + request.url.split("/")[-1]
  authorizedUser = AuthorizedUser()
  if authorizedUser.isAdmin:
    system      = GetSystemManagement()
    data        = request.form
    logList         = system.add_semester(data)
    print logList
    #TODO: figure out how to log
    log.writer(logList[0],page,logList[1])
    flash(logList[1])
    return redirect(redirect_url())
      
                            