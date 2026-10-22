"""Small fictional dataset shared by tests and explicitly invoked local demos.

Call seed_demo_data() only after creating empty tables in the intended database.
Importing this module never connects, creates tables, or inserts records.
"""
from datetime import date, timedelta


def seed_demo_data(today=None):
    from app.models import (mainDB, Semesters, Divisions, Programs, Users,
                            Courses, UsersCourses, Deadline)

    today = today or date(2026, 10, 1)
    records = {}
    with mainDB.atomic():
        records['previous_term'] = Semesters.create(SEID=202512, year=2026, term='Spring')
        records['current_term'] = Semesters.create(SEID=202611, year=2026, term='Fall')
        for name in ('science', 'arts'):
            records[name] = Divisions.create(name=name.title())
        records['computing'] = Programs.create(name='Computer Science', DID=records['science'])
        records['history'] = Programs.create(name='History', DID=records['arts'])
        roles = {
            'admin': {'isAdmin': True},
            'division_chair': {'DID': records['science']},
            'program_chair': {'PID': records['computing']},
            'faculty': {},
            'other_faculty': {},
        }
        for username, role in roles.items():
            records[username] = Users.create(
                username=username, firstName=username.replace('_', ' ').title(),
                lastName='Example', email=username + '@example.test', **role)
        for name, prefix, program, term, instructor, path in (
            ('faculty_course', 'CSC', 'computing', 'current_term', 'faculty', None),
            ('archived_course', 'CSC', 'computing', 'previous_term', 'faculty', '/demo/archived.pdf'),
            ('other_course', 'HIS', 'history', 'current_term', 'other_faculty', None),
        ):
            records[name] = Courses.create(
                prefix=prefix, number='226', section='A', PID=records[program],
                SEID=records[term], filePath=path,
                lastModified='Demo syllabus' if path else None)
            UsersCourses.create(username=records[instructor], CID=records[name])
        for name, offset in (('past_deadline', -1), ('future_deadline', 7)):
            records[name] = Deadline.create(description=name.replace('_', ' '),
                                            date=today + timedelta(days=offset))
    return records
