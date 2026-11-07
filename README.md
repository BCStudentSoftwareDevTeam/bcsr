## Built With

* [Flask](http://flask.pocoo.org/docs/0.11/)  - Python Based Web Framework Used
* [Jinja2](http://jinja.pocoo.org/docs/dev/) - HTML Templating Language for Python
* [Peewee](http://docs.peewee-orm.com/en/latest/index.html) - A small, expressive ORM used for database communications
* [MySQL](https://www.mysql.com/) - SQL database engine

## Requirements
* python 3.11+
* linux, unix, mac, windows (with WSL)
* git

> **Note:** The setup steps below were written for the environment of the contributor who wrote them. If you are setting up on macOS, Windows, or Docker and run into OS-specific differences, please note them here.

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

## Setting Up on Linux

### 1. Install Python

Check your Python version:
```bash
python3 --version
pip3 --version
```

If Python is not installed (Debian/Ubuntu):
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### 2. Install MySQL

- Check whether MySQL is already installed: ```mysql --version```
- If it is not installed (Debian/Ubuntu):
```bash
sudo apt install mysql-server
sudo service mysql start
```
- Test the connection: ```mysql -u root -p```

>Afterwards, go to: Running BCSR after the setup section

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

### 2. Verify Database Connection
#### 2.1 Check MySQL is Running

For MacOS:
- Check MySQL is running: ```brew services list```
- If MySQL is stopped: ```brew services start mysql```

For Windows PowerShell (Administrator):
> **Note:** For window users `*mysql*` finds all mysql and you will see

- Check MySQL is running: Get-Service *mysql*
- Example:

| Status  | Name    | Display Name |
|---------|---------|--------------|
| Running | MySQL80 | MySQL80      |
| Stopped | MySQL84 | MySQL84      |

- Start the required service with: ```Start-Service MySQL80``` (Replace MySQL80 with your service name).

#### 2.2 Test the MySQL Login

- Run: ```mysql -u root -p```
- If your password is root: ```mysql -u root -proot```
- A successful connection will show: ```mysql>```

#### 2.3 Check the BCSR Database

- Inside MySQL: ```SHOW DATABASES;```
- If bcsr does not exist: 
```mysql
CREATE DATABASE bcsr; 
USE bcsr;
```

#### 2.4 Check Permissions

Run: 
```mysql
SELECT USER(), CURRENT_USER(); 
SHOW GRANTS FOR CURRENT_USER;
```
If you see: 
```mysql
GRANT ALL PRIVILEGES ON `bcsr`.* TO `root`@`localhost`
or
GRANT ALL PRIVILEGES ON *.* TO `root`@`localhost`
```
then the user already has the required access.

If the access is missing, grant it with:
```mysql
GRANT ALL PRIVILEGES ON bcsr.* TO 'root'@'localhost'; FLUSH PRIVILEGES;
```

#### 2.5 Verify MySQL Authentication Method

Check which authentication plugin you are using:
```mysql
SELECT user, host, plugin
FROM mysql.user
WHERE user = 'root';
```

You may see something like: ```root | localhost | caching_sha2_password```

Modern MySQL commonly uses: ```caching_sha2_password```.

If the root account needs to be reset to use SHA authentication and the correct password, run:

```mysql
ALTER USER 'root'@'localhost'
IDENTIFIED WITH caching_sha2_password BY 'root';
```

Then refresh the privileges: ```FLUSH PRIVILEGES;```

Verify again:
```mysql
SELECT user, host, plugin FROM mysql.user WHERE user = 'root';
```

The result should show: ```root | localhost | caching_sha2_password```

Then test the login again: ```mysql -u root -p```

### 3. Create the Secret Config

The application reads its database credentials and secret key from `app/secret_config.yaml`, which is not tracked in Git. Create it from the example:

```bash
cp app/example_secret_config.yaml app/secret_config.yaml
```

Then edit `app/secret_config.yaml` and set `secret_key` to a value of your own, along with the MySQL `db_name`, `host`, `username`, and `password` for your local database.

> **Note:** `setup.sh` tries to make this copy for you, but it looks for the example file in the wrong place, so copy it manually as shown above.

### 4. Create the Database Tables
> **Warning** Make sure in your secret_config.yaml the password and username under `db` match your MySQL installation values.

Create the empty database first if it does not exist yet (see step 2.3), then build the tables:
```bash
python mysql_migration.py
or
python3 mysql_migration.py
```

> **Note:** Do not use `create_db.py` for this. It is left over from when this project used SQLite and does not work against the current MySQL configuration.

### 5. View the Database

Connect to MySQL: 
```bash
mysql -u root -proot
```

Once connected, you should see the MySQL prompt: 
```bash
mysql> 
```

### 6. Run the Application

Start BCSR with:
```bash
python app.py
or
python3 app.py
```

The terminal will display a local URL. Open that URL in your browser to access the application.

## Testing

Install the dependencies in your virtual environment:

```bash
source venv/bin/activate
python -m pip install -r requirements.txt
```

Run from the repository root. Unit tests do not require a running database or
`app/secret_config.yaml`:

```bash
tests/run_tests.sh unit
```

The current suite covers configuration loading and academic-year semester codes.
It runs without a MySQL server. Application workflow tests will be added in
separate issues under epic #108.

### MySQL fixtures for future integration tests

The reusable fixtures support real MySQL using a disposable database. To use them
in a future integration test, use a local/development server and a dedicated test
account. As a MySQL administrator, create the account once (choose your own password):

```sql
CREATE USER 'bcsr_test'@'localhost' IDENTIFIED BY 'choose-a-test-password';
GRANT ALL PRIVILEGES ON `bcsr\_test\_%`.* TO 'bcsr_test'@'localhost';
```

The grant covers only databases beginning with the literal `bcsr_test_` prefix.
Export the connection settings in your shell; do not put them in the normal
secret configuration:

```bash
export BCSR_TEST_MYSQL_HOST=127.0.0.1
export BCSR_TEST_MYSQL_PORT=3306
export BCSR_TEST_MYSQL_USER=bcsr_test
export BCSR_TEST_MYSQL_PASSWORD='choose-a-test-password'
# Optional, for a local socket instead of TCP:
# export BCSR_TEST_MYSQL_SOCKET=/path/to/mysql.sock

tests/run_tests.sh all
tests/run_tests.sh unit -k semester
```

The runner forwards pytest options and returns a nonzero exit status on failure.
Direct `python -m pytest` uses the same fixtures. Missing MySQL access is an error
for integration tests, not a silent skip.

### Isolation and demo data

`tests/conftest.py` supplies a temporary `BCSR_SECRET_CONFIG` before importing the
application. Normal startup still defaults to `app/secret_config.yaml`; the test
suite never reads or edits it. Tests requesting the MySQL fixtures create a
uniquely named `bcsr_test_<uuid>` database and remove it at teardown. Tables and demo records
are rebuilt for each database test, so tests do not depend on execution order.
An interrupted/killed process may leave its uniquely named database behind;
remove that specific database manually if needed.

Uploads, download fixtures, generated files, and request logs use pytest's
temporary directories. Tests authenticate through the existing `eppn` request
environment and Flask test client, so no browser or login server is required.

`database/demodata.py` provides `seed_demo_data(today=None)`. It creates fictional
users for every role, two divisions/programs, two semesters, linked courses with
and without a syllabus, and deadlines. It returns a dictionary of named model
objects so tests need not assume generated IDs. Its default date is fixed for
repeatability; callers can pass a date when testing deadline behavior. Importing
it does not write data. Call it explicitly only after creating empty tables in
the intended demo/test database. It creates database records; file fixtures are
created separately by the test client fixture. Do not run `create_db.py` to
prepare tests.

Add self-contained checks to `tests/unit/` with `pytest.mark.unit`, and database
or Flask workflow checks to `tests/integration/` with `pytest.mark.integration`.
Use `demo_data`, `client`, and `login` from `conftest.py` for shared setup. The
current suite covers configuration loading and academic-year term codes; role,
search, and upload workflow tests are outside this PR. The integration category
currently contains no tests; selecting it alone returns pytest's no-tests exit code.
