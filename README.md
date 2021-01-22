# **GOT IT FINAL PROJECT**

This is the final project for the Onboarding Program for Backend Intern 
at Got It. In this mini-application, user can sign in, sign up and 
create, view, update, delete items and categories. This is a RESTful API 
built with Python, MySQL database (SQLAlchemy for ORM), and Flask.



## Prerequisite

Make sure you have already installed all of the following programs:
+ MySQL, https://dev.mysql.com/downloads/mysql/
+ Python (3.0 or later), https://www.python.org/getit/
+ pip, https://pip.pypa.io/en/stable/installing/

## Installation
#### 1. Clone this repository
#### 2. Go to the root directory of this repository on your local machine:
`cd GotItFinalProject`
   
#### 3. Create virtual environment:

   `pip install virtualenv`
   
   `virtualenv venv -python=python3`

   `source venv/bin/activate`

#### 4. Install required packages:
   
   `pip install -r requirements.txt`

#### 5. Setup database

Create 2 MySQL database for 2 different environments: development and test

Go to the corresponding config file under GotItFinalProject/main/config/ and
change the SQLALCHEMY_DATABASE_URI base on your personal database:

   `SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{passowrd}@localhost:3306/{database_name}"`

E.g:    
`SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:mathefuka1@localhost:3306/dev"`

After that, run the following command to create database tables:

`python create_tables.py`

#### 6. Start the app

Type the following command to in your terminal:
`python run.py`

#### 7. Testing

To test the app, type the following command in your terminal, a detail 
will be generated under htmlcov/index.html:

`FLASK_ENV=test coverage run -m pytest`

`coverage html`



