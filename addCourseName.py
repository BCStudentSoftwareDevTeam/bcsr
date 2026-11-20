from playhouse.migrate import MySQLMigrator, migrate
from app.models import mainDB, Courses

migrator = MySQLMigrator(mainDB)
migrate(migrator.add_column('courses', 'name', Courses.name))
print("added courses.name")