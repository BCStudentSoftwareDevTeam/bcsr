from allImports import *

def get_user( user_name ):
    user        = (Users
                        .select()
                        .where(
                                Users.userName == user_name
                   )).get()
    return user



