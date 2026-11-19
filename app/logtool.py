from flask import Flask, request
from datetime import datetime
import os.path
import os

class Log():

    def __init__(self, logfile = 'urcpp.log'):
        here = os.path.dirname(__file__)
        self.logfile = os.path.join(os.path.join(here,logfile))
        self.lowPrivilege = "User does not have enough access privileges for this operation"
    def writer(self, level, page, message):
        try:
            from app.allImports import authUser
            username = authUser(request.environ)
        except Exception:
            username = None

        if not username:
            username = (
                request.environ.get("eppn")
                or request.environ.get("HTTP_EPPN")
                or request.environ.get("HTTP_X_PROXY_REMOTE_USER")
                or request.environ.get("REMOTE_USER")
            )
        if username:
            username = username.split("@")[0].split("/")[-1].lower()
        else:
            username = "unknown"
        # username = os.environ[envK]
        log = open(self.logfile, 'a')
        ip      = request.remote_addr
        date    = datetime.today()
        logInfo = '[{0}] [{1}] [{2}] [{3}] [{4}] {5} \n'.format(str(date), level, ip, username ,page,  message)
        print(logInfo)
        log.write(logInfo)
        log.close()

        try:
            from app.models import ActivityLog
            ActivityLog.create(
                timestamp=date,
                actor=username,
                action=ActivityLog.simplify_action(message)
            )
        except Exception as error:
            print("Unable to persist activity log: {0}".format(error))
