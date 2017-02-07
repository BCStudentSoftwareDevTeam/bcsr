from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url

@app.route("/admin/courseManagement", methods=["GET"])
def courseManagement():
    authorizedUser = AuthorizedUser()
    return render_template('admin/courseManagement.html',
                            cfg = cfg,
                            isAdmin       = authorizedUser.isAdmin,
                            )