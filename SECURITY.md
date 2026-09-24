# Security Policy

BCSR (Berea College Syllabus Repository) holds real course, faculty, and syllabus data for
Berea College. Treat anything that could expose that data — or let someone act as a user
they are not — as a security issue.

## Reporting a Vulnerability

**Do not open a public issue for a security vulnerability.** A public report tells everyone
about the problem before it can be fixed.

Email both maintainers directly instead:

* [@sheggen](https://github.com/sheggen) — heggens@berea.edu
* [@brianramsay](https://github.com/brianramsay) — ramsayb2@berea.edu

Please include:

* What the problem is, and which page, route, or file it affects.
* The steps to reproduce it, including the role you were acting as (administrator, division
  chair, program chair, or faculty).
* What someone could do with it — read data they should not see, change or delete records,
  upload or download files, act as another user.
* Anything you already know about a fix.

## What to Expect

This project is maintained by faculty and students at Berea College, so response times move
with the academic calendar. We aim to acknowledge a report within a few business days during
the semester; replies over breaks may take longer. If the report is valid we will work on a
fix, keep you posted, and credit you when it is disclosed unless you would rather stay
anonymous.

## Scope

Worth reporting:

* Access control failures — reaching a page, syllabus, or action reserved for another role.
* Anything that exposes student, faculty, or course data to someone who should not see it.
* Injection, cross-site scripting, or file upload handling that lets arbitrary content run.
* Credentials or secret keys committed to the repository or readable from a deployed server.

Not vulnerabilities on their own: the development configuration is intentionally permissive.
`DEBUG.user` in `app/config.yaml` fakes the logged-in user for local development, and
`app/example_secret_config.yaml` ships with placeholder credentials that are never used in
production.
