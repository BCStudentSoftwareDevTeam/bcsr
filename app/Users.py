from allImports import *

def getUID( un, users=Users ):
    UserId = users.query.filter_by(username=un).first()
    return UserId.UID
    #return 0

def getRID( un ):
    #uid     = getUID( un )
    #role    = User_role.query.filter_by(UID = uid)
    #return role.RID
    return 1