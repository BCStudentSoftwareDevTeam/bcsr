from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url

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
        SEID = data['SEID']
        courses = UsersCourses.select().join(Courses).where(Courses.filePath >> None)
        for course in courses:
            print course.CID, course.CID.prefix, course.username, course.username.firstName
    except Exception as e:
        #TODO: Log e
        flash('Error occured while trying to prepare excel sheet. ')
    return redirect(url_for("missingSyllabi"))
    