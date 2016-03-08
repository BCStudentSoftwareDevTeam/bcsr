# This is the home page for bcsr
from allImports import *
@app.route("/", methods = ["GET"])
def start():
    #TODO: FIND OUT HOW TO CATCH THE USERNAME FROM THE LOGIN PROCESS
    #TODO: NEED TO FIGURE OUT HOW TO HANDLE SESSION VARIABLES IN FLASK
    #TODO: THEN WE NEED TO STORE THE PROPER SESSION VARIABLES HERE
    return render_template("start.html",
                            cfg = cfg)