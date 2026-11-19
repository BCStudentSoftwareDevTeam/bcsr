from app.allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.models import ActivityLog


@app.route("/admin/activityLog", methods=["GET"])
@app.route("/activityLog", methods=["GET"])
def activityLog():
    authorizedUser = AuthorizedUser()
    if not authorizedUser.isAdmin:
        abort(403)

    ActivityLog.create_table(safe=True)
    entries = ActivityLog.select().order_by(ActivityLog.timestamp.asc())
    return render_template(
        "admin/activityLog.html",
        cfg=cfg,
        isAdmin=True,
        currentPage="Activity Log",
        entries=entries
    )
