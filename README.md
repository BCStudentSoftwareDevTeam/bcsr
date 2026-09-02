## Built With

* [Flask](http://flask.pocoo.org/docs/0.11/)  - Python Based Web Framework Used
* [Jinja2](http://jinja.pocoo.org/docs/dev/) - HTML Templating Language for Python
* [Peewee](http://docs.peewee-orm.com/en/latest/index.html) - A small, expressive ORM used for database communications
* [SQLite](https://sqlite.org/) - SQL database engine

## Requirements
* python 3.11+
* linux, unix, mac, windows(with attachments)
* git

## Setting Up a Linux Environment on Windows
### 1. Install WSL and Ubuntu

Open PowerShell as Administrator and check: 
```bash 
wsl --status
wsl -l -v
```

If WSL is not installed: ```wsl --install```
After it is completed run ```wsl -l -v``` to see if Ubuntu is installed.
If Ubuntu is not installed run: ```wsl --install -d Ubuntu```, then restart your laptop afterwards.

Then launch Ubuntu with: ```wsl```.

### 2. Install MySQL

- Check whether MySQL is already installed in PowerShell: 
```mysql --version ```. 
- You can also check the MySQL installation directory: ```Get-ChildItem "C:\Program Files\MySQL" -ErrorAction SilentlyContinue ```. 
- From WSL, you can check the Windows MySQL installation in bash with: ```ls "/mnt/c/Program Files/MySQL" ```.
- If MySQL GUI is not installed, download the MySQL Installer: https://dev.mysql.com/downloads/installer/
- You will see the prompt to log in or sign up instead choose “No thanks, just start my download.”
- During the installation process, you will be given the option to select client, server or both and you should choose both.

### 3. Install Python

From WSL/Ubuntu check if python is installed: 
```bash
python3 --version
pip3 --version
```

If Python is not installed:
``` bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

After installation, verify it again: ```python3 --version```

>Afterwards, go to: Running BCSR after the setup section


## Setting Up a Linux Environment on MacOS
### 1. Install Homebrew

Check whether Homebrew is installed:
```bash 
brew --version
```
- If you receive: ```command not found: brew```
- Install Homebrew by running the following command in Terminal:  ```/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"```
- Then verify: ```brew --version```

### 2. Install MySQL

- Check whether MySQL is installed: 
```bash
mysql --version
brew list | grep mysql
```
If MySQL is not installed go to the MySQL Community Server download page: https://dev.mysql.com/downloads/mysql/

Download the correct DMG:
- Apple Silicon: ARM64
- Intel Macs: x86_64

During setup, configure the MySQL root account. BCSR commonly uses:
- Username: root
- Password: root

If you use a different password, update app/secret_config.yaml.

Test the connection: ```mysql -u root -p```

### 3. Install Python

Check you installed Python version and pip: 
```bash
python3 --version
pip3 --version
```

If Python is not installed: ```brew install python```

## Running BCSR after the setup

Navigate to your BCSR repository e.g.: ```cd ~/Desktop/SSDT/bcsr```

### 1. Activate the Virtual Environment

On Windows, first enter WSL: 
```bash
wsl
```

Then, on either Windows/WSL or macOS, run:
``` bash
source setup.sh
```

You should see (venv) at the beginning of your terminal prompt.

- During the setup, if you have this error: `-bash: setup.sh: line <something>: syntax error: unexpected end of file from "if" command on line 19` go to the bottom of your IDE and find CRLF and click it to select  LF

>***Note:*** 
In order for the application to work, you must activate the virtual environment. 

>***Note:***
Also, If you ever want to deactivate the virtual environment for any reason just type ```deactivate``` into the terminal.

### 2. Create the Database
> **WARNING:** `create_db.py` is intended for development setup. Do not run this script against a production environment after real data exists.

Run:
```bash
python create_db.py
or 
python3 create_db.py
``` 

### 3. View the Database

Connect to MySQL: 
```bash
mysql -u root -proot
```

Once connected, you should see the MySQL prompt: 
```bash
mysql> 
```

### 4. Run the Application

Start BCSR with:
```bash
python app.py
or
python3 app.py
```

The terminal will display a local URL. Open that URL in your browser to access the application.

## Working with the flask template ##
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

[TOC]
#Installation#
