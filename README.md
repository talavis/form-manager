Form Manager
============

A simple system (backend/frontend) to receive form submissions.

Login is performed using OpenID connect. There is no internal user account management.

When a form is added, it will be given a unique ID. Form submission can then be done using POST to `/api/v1/form/<identifier>/incoming`. The full url for submissions is also available:  `/api/v1/form/<identifier>/url`.

Features:
* Send the form submission to an email address
* Recaptcha validation (v2 confirmed to work)
* Redirection to wanted page after submission

## Setup

See `docker-compose.yml`.

* Mongo database
* Backend (Flask)
* Frontend (Quasar)
