from allImports import *
from app.logic import databaseInterface
from app.logic.getAll import GetAll

@app.route("/archive/", defaults={'SEID': None}, methods = ["GET", "POST"])
@app.route("/archive/<SEID>", methods = ["GET", "POST"])
def archive(SEID):
    semesters = databaseInterface.grab_all_semesters()
    if SEID == None:
        SEID = databaseInterface.grab_current_semester()
    
    
    
    
        
    return render_template("archive.html",
                        cfg = cfg,
                        semesters = semesters,
                        SEID      = SEID
                        )
  