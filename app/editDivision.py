from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url
@app.route("/editDivision", methods=["POST"])
def editDivision():
    authorizedUser = AuthorizedUser()
    if authorizedUser.isAdmin:
      
      # we need the page for logging purposes
      page        = "/" + request.url.split("/")[-1]
      data        = request.form
      newChairs   = request.form.getlist('professors[]')
      did         = data['DID']
      #SELECT ALL OF THE CURRENT CHAIRS OF THE DIVISION
      currentChairs = Users.select().where(Users.DID == did)  
      
      for currentChair in currentChairs:                                      
        # we want to delete chairs that are not in the new list
        if currentChair.username not in newChairs:                   
          message = "USER: {0} has been removed as a Division chair for did: {1}".format(currentChair.username,did)
          log.writer("INFO", page, message)
          currentChair.DID = None
          currentChair.save()
        # we dont want to duplicate chairs
        else:
          newChairs.remove(currentChair.username)                  
          
      for user_name in newChairs:                                           
        #ADD THE USERNAMES TO THE Division CHAIR LIST
        newChair = Users.get(Users.username == user_name)
        newChair.DID = did 
        newChair.save()
        message = "USER: {0} has been added as a Division chair for did: {1}".format(user_name,did)
        log.writer("INFO", page, message)
        
      flash("Division succesfully changed")
      return redirect(redirect_url())
    else:
      abort(403)