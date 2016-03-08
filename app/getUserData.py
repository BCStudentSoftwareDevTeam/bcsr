from allImports import *

def getUID( un ):
    UserId = Users.query.filter_by(username=un).first()
    return UserId.UID

def getRID( un ):
    uid     = getUID( un )
    role    = User_role.query.filter_by(UID = uid)
    return role.RID