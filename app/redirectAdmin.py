from allImports import *

@app.route("/redirect/program_management", methods=["GET"])
def redirectProgramManagement():
   program = Programs.get()
   
   return redirect(url_for("adminProgramManagement", 
                           pid = program.PID, ))

@app.route("/redirect/division_management", methods=["GET"])
def redirectDivisionManagement():
   division = Divisions.get()
   
   return redirect(url_for("adminDivisionManagement", 
                           did = division.DID, ))