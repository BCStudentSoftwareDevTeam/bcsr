from allImports import *
from app.logic.getAuthUser import AuthorizedUser
import datetime
import time

@app.route("/admin/systemManagement", methods=["GET", "POST"])
def systemManagement():
  authorizedUser = AuthorizedUser()
  if authorizedUser.isAdmin:
    semesters = Semesters.select()
    today     = datetime.date.today()
    #We want the user to have the ability to select a year ago and 
    #three years ahead of the current year
    years = []
    #start with one year ago
    year  = int(time.strftime("%Y")) - 1   
    for x in range(5):
      if x == 0:
        years.append(str(year))
      year + 1
      years.append(str(year))
    return render_template('admin/editSystem.html',
                            cfg = cfg,
                            semesters = semesters,
                            years     = years
                            )