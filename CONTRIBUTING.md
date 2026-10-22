# Contributing to BCSR

Thanks for your interest in contributing! BCSR (Berea College Syllabus Repository) is a
Flask application maintained by the Berea College Student Software Development Team. It
lets faculty upload syllabi and lets division chairs, program chairs, and administrators
track which syllabi are still missing each term.

This document explains the conventions we follow and how to get your work reviewed and
merged. For setting up a development environment, follow the setup instructions in the
[README](README.md).

## Table of Contents

* [Code of Conduct](#code-of-conduct)
* [Ways to Contribute](#ways-to-contribute)
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
questions before assuming a mistake. Report unacceptable behavior to a maintainer:
[@sheggen](https://github.com/sheggen) (heggens@berea.edu) or
[@brianramsay](https://github.com/brianramsay) (ramsayb2@berea.edu).

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
* **Review a pull request.** Read through someone else's open pull request, test their
  changes, and leave a review. Student reviews are how pull requests get ready for a
  maintainer, and reviewing is a good way to learn the codebase.

Before starting work on an issue, comment on it so it can be assigned to you. This keeps two
people from writing the same patch.

## Development Workflow

### Get the code

How you get the code depends on whether you have write access to
`BCStudentSoftwareDevTeam/bcsr`. Student Software Development Team members usually do;
outside contributors usually do not. **If you are not sure, fork.** Forking always works,
and nothing is lost if it turns out you had write access after all.

**With write access,** clone the repository directly:

```bash
git clone git@github.com:BCStudentSoftwareDevTeam/bcsr.git
cd bcsr
git remote add upstream git@github.com:BCStudentSoftwareDevTeam/bcsr.git
```

**Without write access,** fork the repository on GitHub, then clone your fork:

```bash
git clone git@github.com:<your-username>/bcsr.git
cd bcsr
git remote add upstream git@github.com:BCStudentSoftwareDevTeam/bcsr.git
```

Either way you end up with a remote named `upstream` pointing at the main repository, so
every other command in this guide works the same for both. If you cloned directly, `origin`
and `upstream` point at the same repository — that is intentional, not a mistake.

Then follow the setup instructions in the [README](README.md) for your system (Windows
through WSL, macOS, or Linux) and start the application once to make sure everything runs
before you change anything.

### Branch from `development`

`development` is the default branch and the target for all pull requests. `master` is the
production branch; do not open pull requests against it.

```bash
git checkout development
git pull upstream development
git checkout -b <issue-number>_<short-description>
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

Match the surrounding code. Naming conventions are not uniform across this codebase —
Python, JavaScript, and test files each follow their own — so the naming examples below
describe what is already in use rather than strict rules. When you name a variable, look
at the variables around it and use the same naming convention they use. When you name a
function, make the name an abstract of what the function does, and again match the
functions around it.

**Python**

* Two-space indentation.
* A docstring at the top of each module and class explaining its purpose.
* You will see `CapWords` class names (`GetCourses`, `AuthorizedUser`), `camelCase` route
  functions and local variables (`semesterManagement`, `currentSEID`), and `snake_case`
  logic and database helper methods (`get_all_semesters`, `check_for_my_courses`). Follow
  whichever pattern the file you are editing already uses.

**Database models** (as documented in `app/models.py`)

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

1. Push your branch to `origin` — your fork if you forked, the main repository if you
   cloned directly:

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

Both maintainers are requested for review automatically through
[`.github/CODEOWNERS`](.github/CODEOWNERS), and one of them will merge your pull request
once it is approved. If you are a student contributor, add yourself to the `contributors`
list in `app/config.yaml` with your name, username, and year as part of your first pull
request.

## Security and Secrets

* **Never commit `app/secret_config.yaml`.** It is listed in `.gitignore`; keep it that way.
* Never commit real database credentials, secret keys, or student data in any file,
  including test fixtures, comments, and screenshots.
* Uploaded syllabi under `app/static/files/` are untracked and must stay that way.
* If you find a security vulnerability, do **not** open a public issue. Follow
  [`SECURITY.md`](SECURITY.md): email [@sheggen](https://github.com/sheggen)
  (heggens@berea.edu) and [@brianramsay](https://github.com/brianramsay)
  (ramsayb2@berea.edu) directly so it can be fixed before it is disclosed.

## Getting Help

* Check the [README](README.md) for background on the stack and the original setup notes.
* Ask in the issue you are working on — a question on the issue is visible to everyone and
  helps the next contributor who hits the same problem.
* If your development environment will not start, include the full command you ran and the
  complete error output when you ask.
* The maintainers are [@sheggen](https://github.com/sheggen) (heggens@berea.edu) and
  [@brianramsay](https://github.com/brianramsay) (ramsayb2@berea.edu). Reach out directly if
  you are blocked on something the issue thread cannot resolve.

Thanks for contributing!
