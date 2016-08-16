from allImports import *
from app.logic.getAuthUser import AuthorizedUser
import datetime


@app.route("/", methods=["GET", "POST"])
def deadlineDisplay():
    if (request.method == "GET"):
        authorizedUser = AuthorizedUser()

        # we don't want to show deadlines past today
        today = datetime.date.today()
        
        # we don't want show repeated dates
        dates = Deadline.select(
            Deadline.date).where(Deadline.date > today).distinct().order_by(
            Deadline.date)

        deadlines = []
        for date in dates:
            # assign the deadline object to a date for easy access
            deadlines.append(
                (date.date, Deadline.select().where(
                    Deadline.date == date.date)))

    return render_template("deadline.html",
                           cfg=cfg,
                           isAdmin=authorizedUser.isAdmin,
                           deadlines=deadlines,
                           today=today)
