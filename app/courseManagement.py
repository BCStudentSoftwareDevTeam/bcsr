from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url

@app.route("/admin/courseManagement", methods=["GET"])
def courseManagement():
    authorizedUser = AuthorizedUser()
    return render_template('admin/courseManagement.html',
                            cfg = cfg,
                            isAdmin       = authorizedUser.isAdmin
                            )

@app.route("/admin/courseManagement/missingSyllabi", methods=["GET"])
def missingSyllabi():
    authorizedUser = AuthorizedUser()
    activePage = "snips/missingSyllabi.html"
    # activePage should be the name of the snip that should contain the content
    # of the page-wrapper section of courseMangement.html
    semesters = Semesters.select()
    return render_template('admin/courseManagement.html',
                            cfg           = cfg,
                            isAdmin       = authorizedUser.isAdmin,
                            activePage    = activePage,
                            semesters     = semesters)
    