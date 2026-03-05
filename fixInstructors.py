# This file was created to fix broken relationships between the users and courses. 
# The error was created when the remove course feature was added. The course was removed, but the relationship 
# between the user and course was not, which eventually caused users to be assigned to 
# courses that were not theirs. This file fixed those errors by deleting the relationship. 
# It should not be needed again.

from app.models import *

def clean(inCID, user):
	UsersCourses.delete().where(UsersCourses.CID == inCID, UsersCourses.username == user).execute()

cids = [13433,13434,13435,13436,13437,13438,13439,13440,13441,13442,13442,13443,13444, 13444,13445,13445,13446,13447,13448,13449,13450,13451,13451,13452,13453,13453,13454,13454,13455,13456,13457,13458,13458,13459,13460,13461,13461,13462,13463,13464,13464,13465,13466,13467,13467,13468,13469,13470,13470,13471,13471,13472,13472,13473,13473,13474,13475,13476,13476,13477,13432,13432,13432,13432]
users = ["baskina", "mortaraa", "grattonl", "bolsterst", "kennisonm", "lambc", "lambc", "kennisonm", "heyrmanj", "heyrmanj", "boumaj", "messerw", "messerw", "smithro", "burnsidej", "feaganb", "woodwarda", "woodwarda", "burnsidej", "woodwarda", "martinde", "masonq", "rivage-seulp", "derossetf", "nakazawam", "heggens", "messerw", "boumaj", "hackbertp", "mortaraa", "cupidonj", "nakazawam", "heggens", "mcdonaldv", "boumaj", "guggenheimd", "hackbertp", "graetzerm", "parrm", "blanks", "boumaj", "riversk", "lambc", "nakazawam", "heggens", "brownke", "lambc", "nakazawam", "heggens", "norrisj", "hackbertp", "masonq", "rivage-seulp", "dickersonj", "hackbertp", "cupidonj", "blythej", "woodwarda", "boumaj", "derossetf", "tudora", "tudora", "tudora", "webba"]

index = 0
for cid in cids:
#	print(index, cid, users[index])
	clean(cid, users[index])
	index += 1

