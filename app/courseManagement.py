from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url
from app.logic.excelMaker import makeExcelFile
from flask import send_file

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
                            
@app.route("/admin/courseManagement/missingSyllabi", methods=["POST"])
def findMissingSyllabi():
    try:
        data = request.form
        filePath = makeExcelFile(data['SEID'])
        return send_file(filePath,as_attachment=True)
    except Exception as e:
        #TODO: Log e
        print e
        flash(e)
        flash('Error occured while trying to prepare excel sheet. ')
        return redirect(url_for("missingSyllabi"))
    