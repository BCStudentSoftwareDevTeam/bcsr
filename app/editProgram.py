from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url
@app.route("/editProgram", methods=["POST"])
def editProgram():
    authorizedUser = AuthorizedUser()
    if authorizedUser.isAdmin:
      page        = "/" + request.url.split("/")[-1]
      data        = request.form
      newChairs   = request.form.getlist('professors[]')
      pid         = data['PID']
      
      #SELECT ALL OF THE CURRENT CHAIRS OF THE PROGRAM
      currentChairs = Users.select().where(Users.PID == pid)
      #LOOP THROUGH ALL OF THE CURRENT CHAIRS
      # print 'hello', currentChairs
      for currentChair in currentChairs:                                    
        #IF A USER'S NAME IS NOT PART OF THE NEWCHAIR LIST THEN DELETE THEM
        if currentChair.username not in newChairs:                 
          message = "USER: {0} has been removed as a program chair for pid: {1}".format(currentChair.username ,pid)
          log.writer("INFO", page, message)
          currentChair.PID = None
          currentChair.save()
        else:
          #HOWEVER IF THEY ARE PART OF THE LIST, DELETE THEM FROM THE LIST
          newChairs.remove(currentChair.username)                  
      #LOOK THROUGH THE NEW CHAIR LIST    
      for user_name in newChairs:                                           
        #ADD THE USERNAMES TO THE PROGRAM CHAIR LIST
        newChair  = Users.get(Users.username == user_name)   
        print newChair.username
        newChair.PID = pid     
        newChair.save()
        message = "USER: {0} has been added as a program chair for pid: {1}".format(user_name,pid)
        log.writer("INFO", page, message)
        
      flash("Program succesfully changed")
      return redirect(redirect_url())
        
      
        

     
    
   