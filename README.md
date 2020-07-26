# Kolture-Blog
A simple Django Blogging App

# Features

    User authorisation and registration
    Basic user permissions: admin, users.
        all users can add posts, update and delete post for which they have suitable permissions/ownership.
        admin is superuser.
    Comment system
    You can choose to either Publish Post as Featured Post, Normal Post or leave as Draft
    Sort post by category.
    ckeditor
  
# Main Requirements

    python 3.5, 3.6, 3.7 or higher
    Django 2.1.8 or higher
 
To clone this repository to the current directory:

git clone https://github.com/Kingkellee/Kolture-Blog.git .

Next, set up a virtual environment and activate it:

python3 -m venv env && source env/bin/activate

Install required packages:

Next, perform migration:

python3 manage.py migrate

The setup is complete. Then Run a local server with

python3 manage.py runserver.
