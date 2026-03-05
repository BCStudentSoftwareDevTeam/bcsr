from app.allImports import *
from app.logic import databaseInterface
from app.logic.getAuthUser import AuthorizedUser
from app.logic.getAll import GetAll
from app.models import Semesters

@app.route("/archive/", defaults={'SEID': None}, methods = ["GET", "POST"])
@app.route("/archive/<SEID>", methods = ["GET", "POST"])
def archive(SEID):
    # we need to know if the user is authorized to see this
    authorizedUser = AuthorizedUser()
    getAll = GetAll()
    semesters = databaseInterface.get_all_semesters()
    if SEID == None:
        SEID = databaseInterface.grab_current_semester()
    two_dictionaries      = getAll.create_dictionaries(SEID)
    current_term          = Semesters.get(Semesters.SEID == SEID)

    return render_template("archive.html",
                        cfg          = cfg,
                        semesters    = semesters,
                        current_term = current_term,
                        SEID         = SEID,
                        isAdmin      = authorizedUser.isAdmin,
                        divisions_to_programs = two_dictionaries[0],
                        programs_to_courses   = two_dictionaries[1]
                        )
