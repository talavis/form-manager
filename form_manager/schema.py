"""Schemas."""

def form_entry():
    return {
        "identifier": "",  # str, uuid?, automatic?
        "title": "",  # str
        "email": "",  # str, email address; empty = no email sent
        "email_recipients":  # list of str, email addresses to receive the submission
        "recaptcha": False,  # use recaptcha
    }
