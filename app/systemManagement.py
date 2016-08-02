from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.getSystemManagement import GetSystemManagement

@app.route("/admin/systemManagement", methods=["GET", "POST"])
def systemManagement():
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
                            
@app.route("/admin/systemMangement/add", methods=["POST"])
def addSemester():
  authorizedUser = AuthorizedUser()
  if authorizedUser.isAmin:
    system      = GetSystemManagement()
    data        = request.form
    addSemester = system.add_semester(data)
    if addSemeser != True:
      #Flash error message
      flash(addSemester)
    else:
      flash("Semester successfully created.")
    redirect(redirect_url())
      
                            