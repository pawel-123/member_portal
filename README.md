# Member Portal

Member Portal is a web application that allows members of an insurance company to:
- register an account, login and logout
- submit claims (including multiple file upload)
- view the claims table (sortable and filterable)
- view the claim details (incl. images)

## Technology

Member Portal was my first independent project and it was built with Django.

The [django-multiupload](https://pypi.org/project/django-multiupload/) package was modified locally due to an unresolved issue after renderer argument was removed from widget in Django 2.1 [(source)](https://github.com/Chive/django-multiupload/pull/40).

## Prerequisites

Python 3.8 and git

## Installation

1. Open up Terminal, and go into the directory where you want your local copy,
i.e.
```
cd projects
```

2. Download a copy of the repository
```
git clone https://github.com/pawel-123/member_portal.git
```

3. Go into the repository directory, i.e.
```
cd member_portal
```

1. Create a virtual environment, i.e.
```
python -m venv mp_env
```

5. Start the virtual environment, i.e.
```
source mp_env/bin/activate
```

7. Install all dependencies
```
pip install -r requirements.txt
```

8.  Make migrations to set up the database
```
python manage.py makemigrations
```

9. When this has completed, run these migrations
```
python manage.py migrate
```

10. Create a user profile to login with
```
python manage.py createsuperuser
```

11. Once you have followed the instructions to create a user, run the server
```
python manage.py runserver
```

12. If there were no errors anywhere, you can now go to http://localhost:8000/portal/
in your browser to view a local copy of Member Portal.

## Learnings
- Setting up a Django project from scratch
- Setting  virtual environment
- Creating models, including limiting model field choices
- Setting up user registration, login and logout
- Creating sortable and filterable tables with django-tables2 and django-filters
- Adding a button with URL to a table
- Preselecting form fields based on an argument passed in the URL
- Allowing multiple file upload in forms
- Styling with bootstrap4

## To Do's

- [ ] Write tests
- [ ] Set the claims table row colour based on claim status
- [ ] Allow the download of all claim attachments with one click

