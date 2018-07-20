# This is the home page for bcsr
from allImports import *
@app.route("/", methods = ["GET"])
def start():
    #TODO: FIND OUT HOW TO CATCH THE USERNAME FROM THE LOGIN PROCESS
    un = "hopperg";
    #TODO: NEED TO FIGURE OUT HOW TO HANDLE SESSION VARIABLES IN FLASK
        #TODO: SAVE THE USER'S USERNAME WITHIN A SESSION VARIABLE
        #TODO: ROLE LETTER
    #TODO: THEN WE NEED TO STORE THE PROPER SESSION VARIABLES HERE
    return render_template("index.html",
                            cfg = cfg)