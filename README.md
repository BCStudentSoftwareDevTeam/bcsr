## Built With

* [Flask](http://flask.pocoo.org/docs/0.11/)  - Python Based Web Framework Used
* [Jinja2](http://jinja.pocoo.org/docs/dev/) - HTML Templating Language for Python
* [Peewee](http://docs.peewee-orm.com/en/latest/index.html) - A small, expressive ORM used for database communications
* [SQLite](https://sqlite.org/) - SQL database engine

# Setting Up a Development Environment
### Getting Started On Cloud9 ###
[Cloud9](https://c9.io/?redirect=0) is the preferred tool for our software team while developing and debugging code. However, if you are new to cloud9, they did just recent start requiring a credit card to create an account. Therefore you may not want to use cloud9 as your development environment.  

### Create a Workspace with Bitbucket using SSH Protocol

When you first log into your cloud9 account, select the tab that says **workspaces**. After you open this tab you should see an option to create a new workspace, it should look like the image below.

![creatework.PNG](https://bitbucket.org/repo/bEXb4L/images/4213557604-creatework.PNG) 

After you click the button go ahead and input a name and description for this workspace.

![description.PNG](https://bitbucket.org/repo/bEXb4L/images/2446581179-description.PNG)
![public.PNG](https://bitbucket.org/repo/bEXb4L/images/69137571-public.PNG)

>***Note:*** 
The default for the workspace is to be public, it's important to **NOT** change this default option. The way that our system works is that it creates a virtual environment for the application to run on. The virtual environment requires the use of ports in order to access the application. If you may the workspace private, it can block these ports so that they can not be accessed. There may be a way around this; however, we just find it easier if you let the workspace be public. 

Next, you will want to make sure you choose to clone your repo from bitbucket. You do this by adding your git URL using the SSH.

For Example:
```git@bitbucket.org:<username>/<name_of_Repo>.git```

If you are uncertain what your git ssh URL is you can find it at the top of the bitbucket page if you click the clone option. 

![git clone.PNG](https://bitbucket.org/repo/bEXb4L/images/340042303-git%20clone.PNG)

>***Note***: If you copy and paste this line make sure to remove the ```git clone``` at the front in order to ensure you only get the URL.

After you have entered in the URL, the last portion of the page asked you to choose a template. Please select the python option in order to have the workspace to run correctly. 

![PYTHON.PNG](https://bitbucket.org/repo/bEXb4L/images/3923875225-PYTHON.PNG)

All that is left is to hit the create workspace button and your workspace will be configured correctly.

### Getting Your Development Environment Running

After you have created your workspace, there are three additional steps that you will have to complete before your virtual environment will be completely operational. 

**Step One: Activate Your Virtual Environment**

In order to do this, all you have to do is type: ```source setup.sh``` into the Linux terminal. You might have to wait a minute or two as the tools you need for our application are downloaded into your virtual environment. However, after the setup is completed you should see the words ```(venv)``` at the front of your terminal.

![venv.PNG](https://bitbucket.org/repo/bEXb4L/images/2846617267-venv.PNG) 

>***Note:*** 
In order for the application to work, you must activate the virtual environment. If you are not inside of the virtual environment you will see this error:
![venvError.PNG](https://bitbucket.org/repo/bEXb4L/images/1415469357-venvError.PNG)Whenever you get this error just activate the virtual environment again by entering the command ```source setup.sh```

>Also, If you ever want to deactivate the virtual environment for any reason just type ```deactivate``` into the terminal. 
![deactivate.PNG](https://bitbucket.org/repo/bEXb4L/images/2248015321-deactivate.PNG)

**Step Two: Setup Your Database**

A couple of elements are necessary in order to get your database established. The first step is creating the SQLite file, we can create the file in the desired location through the use of one of our scripts.

**Create Database**

By typing the command ```python reset-db.py``` a database file containing the correct schemas will be created in the data directory with the name ```advancement.sqlite```.

**Populate Database**

The ```reset-db.py``` will only create empty tables for you, in order to populate the database you will need to execute the command: ```python add_dummy.py```. This file will add dummy data to the system so that you can gauge how the system is supposed to run.

**How to View the Database** 

Now that you have the database created and populated with data, you are probably asking yourself how do I see that? Our system development team likes to use a tool called [DB Browser](http://sqlitebrowser.org/). This tool is a visual way of viewing and editing SQLite database files. 

![dbBrowser.PNG](https://bitbucket.org/repo/bEXb4L/images/3023751797-dbBrowser.PNG)

**Step Three: Running the Application**

The only remaining step to getting your development environment deployed is running the actual application. This can be achieved through the command ```python run.py```, when you run this command you should see a URL created for you. 

![run.PNG](https://bitbucket.org/repo/bEXb4L/images/1543001500-run.PNG)

The URL will take you to the application and allow you to see any changes you make to the system. That's all that has to be done in order to get the development environment created and ready for editing.

[TOC]
#Installation#

##Requirements##
* python 2.7
* linux, unix, mac, windows(with attachments)
* git

## Creating Development Environment 

1. ** Fork ** the repository from BitBucket and rename the project 

2. If working on a **local machine**, then clone the repo from your terminal. 

3. If you are working from cloud 9 follow [these steps](https://codymyers93.wordpress.com/2016/03/07/octoprint-working-in-cloud-9/) for directions on how to setup cloud 9 with git.

4. After you have successfully clone the repo. Run:
``` bash
source setup.sh
python app.py
```

If you are successful you will see something like:
``` bash
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
		- starty.py #This an example of where your controllers will go