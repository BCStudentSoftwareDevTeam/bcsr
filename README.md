## Built With

* [Flask](http://flask.pocoo.org/docs/0.11/)  - Python Based Web Framework Used
* [Jinja2](http://jinja.pocoo.org/docs/dev/) - HTML Templating Language for Python
* [Peewee](http://docs.peewee-orm.com/en/latest/index.html) - A small, expressive ORM used for database communications
* [SQLite](https://sqlite.org/) - SQL database engine

# BCSR Application Installation

##Requirements##
* python 2.7
* linux, unix, mac, windows(with attachments), Ubuntu

## Creating Development Environment

1. Clone the BCSR repository (from Github) in your home directory: ```git clone <URL>```

2. If working on a **local machine**, then clone the repo from your terminal.

3. Edit your ```secret_config.yaml``` file.

4. Run ```source setup.sh```


## Creating the database
### PHPMYADMIN
1. Go to http://0.0.0.0/phpmyadmin/ replacing the 0.0.0.0 with your server
2. Log in with the credentials used in secret_config.yaml
3. Click on "New" on top of the sidebar at the left of the screen
4. If there is already a database named "bcsr", drop it
5. Create a new database with the name "bcsr"
6. Run ```python create_db.py```

### MYSQL WORKBENCH
1. Go to MySQL Workbench, log in to your MySQL Connection that you use for SSDT.
2. On the top left corner of the application, click on the fourth icon (a plus and container picture) to create a new schema, name it 'bcsr' and click apply.
3. Run ```python create_db.py```
4. If you are successful you will see the tables and their data in 'bcsr'

## Run the Application
1. Run ```python app.py```
If successful you will see something like this:
Starting application
Running server at http://0.0.0.0:8080/

```
Click the link in your terminal to check if it deployed correctly.

# Working with the flask template #
- bcsr-flask
	- App
		-static
			- js
			- css
			- img
		-templates
			- snips # A directory for partial html files
			- start.html #This is an example of where your html files will go
		-logic
			- files that manipulate the database
		- __init__.py
		- allImports.py
		- config.yaml
		- models.py
