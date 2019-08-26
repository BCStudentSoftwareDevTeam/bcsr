from allImports import *
from app.logic import databaseInterface
from app.logic.getAuthUser import AuthorizedUser
from app.logic.getAll import GetAll


@app.route("/contributors/", methods = ["GET"])
def contributors():
    # we need to know if the user is authorized to see this
  
    return render_template("snips/nameList.html",
                        cfg = cfg

                        )
  