from importlib import*
from app.models import *
from updateChairs import*
# def updateChairs_testsuite():
#     updateChairs("myersco", "Cody","Myers", 0, "myersco@berea.edu", 1 )
#     try:
#         testuser = Users.get(Users.username == "myersco")
#         print(testuser.username)
#         print(testuser.PID == 1)
#         print(testuser.DID == 0)
#     except Exception as e:
#         print e
#         print("Case 1 has failed")
#     updateChairs("heggens", "Scott","Heggen", 0, "myersco@berea.edu", 1 )
#     try:
#         testuser = Users.get(Users.username == "myersco")
#         print(testuser.username)
#         print(testuser.PID == 1)
#         print(testuser.DID == 0)
#     except Exception as e:
#         print e
#         print("Case 2 has failed")
# updateChairs_testsuite()