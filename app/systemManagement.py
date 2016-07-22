from allImports import *
from app.logic.getAuthUser import AuthorizedUser

@app.route("/admin/systemManagement", methods=["GET", "POST"])
def systemManagement():
    authorizedUser = AuthorizedUser()
    if authorizedUser.isAdmin:
        semesters = Semesters.select()
        
        return render_template('admin/editSystem.html',
                                cfg = cfg,
                                semesters = semesters
                                )