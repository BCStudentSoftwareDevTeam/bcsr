# Contributing to BCSR

Thanks for your interest in contributing! BCSR (Berea College Syllabus Repository) is a
Flask application maintained by the Berea College Student Software Development Team. It
lets faculty upload syllabi and lets division chairs, program chairs, and administrators
track which syllabi are still missing each term.

This document explains how to set up a development environment, the conventions we follow,
and how to get your work reviewed and merged.

## Table of Contents

* [Code of Conduct](#code-of-conduct)
* [Ways to Contribute](#ways-to-contribute)
* [Setting Up a Development Environment](#setting-up-a-development-environment)
* [Project Layout](#project-layout)
* [Development Workflow](#development-workflow)
* [Coding Conventions](#coding-conventions)
* [Accessibility Requirements](#accessibility-requirements)
* [Testing Your Changes](#testing-your-changes)
* [Opening a Pull Request](#opening-a-pull-request)
* [Security and Secrets](#security-and-secrets)
* [Getting Help](#getting-help)

## Code of Conduct

We expect everyone involved in this project — contributors, reviewers, and maintainers — to
be respectful, patient, and constructive. Many contributors are students writing their first
production code; assume good faith, critique the code rather than the person, and ask
questions before assuming a mistake. Report unacceptable behavior to a project maintainer.

A formal `CODE_OF_CONDUCT.md` is being added separately; until it lands, the expectations
above apply.

## Ways to Contribute

You do not have to write code to help:

* **Report a bug.** Open an issue describing what you did, what you expected, and what
  actually happened. Include the page or route, your browser, and a screenshot or the
  traceback if you have one.
* **Suggest a feature.** Open an issue explaining the problem the feature solves and who
  benefits (faculty, program chairs, division chairs, or administrators).
* **Improve documentation.** Corrections to the README, this file, or `Accessibility.md`
  are welcome and are a good first contribution.
* **Fix an issue.** Browse the
  [open issues](https://github.com/BCStudentSoftwareDevTeam/bcsr/issues). Issues labeled
  `good first issue` are scoped to be approachable for newcomers.

Before starting work on an issue, comment on it so it can be assigned to you. This keeps two
people from writing the same patch.

## Setting Up a Development Environment

### Requirements

* Python 3
* A MySQL server you can connect to
* Git
* Linux, macOS, or WSL (`setup.sh` is a bash script and assumes a POSIX shell)

### 1. Fork and clone

Fork the repository on GitHub, then clone your fork:

```bash
git clone git@github.com:<your-username>/bcsr.git
cd bcsr
git remote add upstream git@github.com:BCStudentSoftwareDevTeam/bcsr.git
```

### 2. Create the virtual environment

```bash
source setup.sh
```

This creates a `venv/` directory, installs everything in `requirements.txt`, and exports
`FLASK_ENV=development` and `FLASK_RUN_PORT=8080`. When it finishes you should see `(venv)`
at the front of your prompt.

Run `source setup.sh` in every new terminal session before working on the app. To leave the
virtual environment, run `deactivate`.

### 3. Create your secret config

The application reads database credentials and the Flask secret key from
`app/secret_config.yaml`, which is not tracked in Git. Create it from the example:

```bash
cp app/example_secret_config.yaml app/secret_config.yaml
```

Then edit `app/secret_config.yaml` and set `secret_key` to a value of your own along with the
MySQL `db_name`, `host`, `username`, and `password` for your local database.

> **Note:** `setup.sh` attempts this copy itself, but it looks for the example file under
> `app/config/`, which does not exist. Copy the file manually as shown above.

### 4. Create the database tables

Create an empty MySQL database matching the `db_name` in your secret config, then build the
schema:

```bash
python mysql_migration.py
```

You can add a user to work with using `add_user.py` (edit the values in the file first) and
add a term with `addNewTerm.py`.

> **Note:** `create_db.py` is left over from when this project used SQLite and does not work
> against the current MySQL configuration. Use `mysql_migration.py` instead.

### 5. Run the application

```bash
python app.py
```

You should see:

```
Running server at http://0.0.0.0:8080/
```

Open that URL in your browser. In development, the logged-in user is faked by the `DEBUG.user`
setting in `app/config.yaml` — change it to test the application as an administrator, a
division chair, a program chair, or a regular faculty member.

## Project Layout

```
bcsr
├── app.py                  # Entry point; starts the Flask server
├── setup.sh                # Creates the venv and installs dependencies
├── mysql_migration.py      # Creates the MySQL schema
├── requirements.txt
└── app
    ├── __init__.py         # Creates the Flask app; imports every page module
    ├── allImports.py       # Shared imports used across page modules
    ├── models.py           # Peewee models (the database schema)
    ├── config.yaml         # Non-secret config: menus, headers, terms, contributors
    ├── secret_config.yaml  # Untracked: secret key and DB credentials
    ├── loadConfig.py
    ├── <page>.py           # One module per page, holding that page's routes
    ├── logic/              # Business logic and database access helpers
    ├── templates/          # Jinja2 templates
    │   └── snips/          # Reusable partial templates
    └── static/             # css, js, img, and uploaded files
```

The important convention: **routes live in the page modules directly under `app/`, and the
work those routes do lives in `app/logic/`.** Keep view functions thin.

When you add a new page module, import it in `app/__init__.py` — it is not part of the
application until you do.

When you add a new table, add the model class to `app/models.py` *and* list it under
`models.mainDB` in `app/config.yaml`.

## Development Workflow

### Branch from `development`

`development` is the default branch and the target for all pull requests. `master` is the
production branch; do not open pull requests against it.

```bash
git checkout development
git pull upstream development
git checkout -b 109_contributing_guidelines
```

Name your branch after the issue you are working on, followed by a short description —
for example `103_flash_message` or `109_contributing_guidelines`.

### Commit as you go

Write commit messages in the imperative mood, describing what the commit changes:

```
Add CONTRIBUTING.md with setup and workflow guidelines
```

Keep commits focused. A reviewer should be able to read your commits in order and follow
your reasoning.

### Keep your branch current

If `development` moves while you are working, bring those changes into your branch and
resolve any conflicts locally rather than leaving them for the reviewer:

```bash
git fetch upstream
git merge upstream/development
```

## Coding Conventions

Match the surrounding code. The conventions already in use are:

**Python**

* Two-space indentation.
* `CapWords` for class names (`GetCourses`, `AuthorizedUser`).
* `camelCase` for route functions and local variables (`semesterManagement`, `currentSEID`).
* `snake_case` for logic and database helper methods (`get_all_semesters`,
  `check_for_my_courses`).
* A docstring at the top of each module and class explaining its purpose.

**Database models** (documented in `app/models.py`)

| Item | Style | Example |
| --- | --- | --- |
| Class names | CapWords | `Semesters` |
| Primary keys | ALL CAPS | `SEID` |
| Foreign keys | ALL CAPS, matching the key referenced | `Divisions.DID = Programs.DID` |
| Other fields | camelCase | `filePath` |

**Configuration**

Anything a maintainer might reasonably want to change without editing code — menu items,
table headers, allowed file types and sizes, upload paths, term codes — belongs in
`app/config.yaml`, not hard-coded.

**Templates**

Put reusable markup in `app/templates/snips/` and include it rather than duplicating it.

## Accessibility Requirements

**If your change touches HTML, CSS, or JavaScript in any way, you must complete the
accessibility checklist in [`Accessibility.md`](Accessibility.md) before opening your pull
request.**

This is not optional. Any failure in the "Beginner" portion of that checklist must be fixed
before your pull request can be accepted. `Accessibility.md` includes a walkthrough video and
links for setting up a screen reader.

## Testing Your Changes

This project does not yet have an automated test suite — adding one is tracked as its own
issue. Until then, test manually and say what you tested in your pull request:

* Exercise the page you changed as each relevant role (administrator, division chair,
  program chair, faculty) by changing `DEBUG.user` in `app/config.yaml`.
* Check the paths around your change, not just the happy path: empty forms, invalid input,
  and permission failures.
* Watch the console and `app/urcpp.log` for errors and stack traces.
* If you changed the database schema, confirm `python mysql_migration.py` builds it cleanly
  on an empty database.

If you do add tests alongside your change, that is welcome — say so in the pull request.

## Opening a Pull Request

1. Push your branch to your fork:

   ```bash
   git push -u origin <your-branch-name>
   ```

2. Open a pull request against the **`development`** branch of
   `BCStudentSoftwareDevTeam/bcsr`.

3. In the description, include:
   * The issue your work closes (`Closes #109`).
   * What you changed and why.
   * How you tested it, including which roles you tested as.
   * Screenshots or a short recording for anything that changes the interface.
   * Confirmation that you completed the accessibility checklist, if you touched the
     front end.

4. Respond to review feedback by pushing additional commits to the same branch. Do not force
   push after review has started — it makes the reviewer re-read everything.

A maintainer will merge your pull request once it is approved. If you are a student
contributor, add yourself to the `contributors` list in `app/config.yaml` with your name,
username, and year as part of your first pull request.

## Security and Secrets

* **Never commit `app/secret_config.yaml`.** It is listed in `.gitignore`; keep it that way.
* Never commit real database credentials, secret keys, or student data in any file,
  including test fixtures, comments, and screenshots.
* Uploaded syllabi under `app/static/files/` are untracked and must stay that way.
* If you find a security vulnerability, do **not** open a public issue. Contact a project
  maintainer directly so it can be fixed before it is disclosed.

## Getting Help

* Check the [README](README.md) for background on the stack and the original setup notes.
* Ask in the issue you are working on — a question on the issue is visible to everyone and
  helps the next contributor who hits the same problem.
* If your development environment will not start, include the full command you ran and the
  complete error output when you ask.

Thanks for contributing!
