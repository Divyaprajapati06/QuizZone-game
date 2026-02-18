# QuizZone - Django Quiz Web Application

QuizZone is a web-based quiz application developed using Django framework.  
It allows users to register, login and attempt quizzes category-wise.  
The system calculates scores and displays leaderboard rankings.

## Features

-  User Registration & Login Authentication
-  Category-wise Quiz Attempt
-  Leaderboard System
-  Automatic Score Calculation
-  Admin Panel to Manage Questions & Categories
-  Responsive UI using Bootstrap

## Tech Stack

- Python
- Django
- HTML5
- CSS3
- Bootstrap
- SQLite Database

##  How to Run This Project Locally

Follow these steps to run the project on your computer:

### Move into Project Folder

cd QuizZone-game

### Create Virtual Environment (Recommended)

python -m venv venv

### Activate Virtual Environment

For Windows:
venv\Scripts\activate

For Mac/Linux:
source venv/bin/activate

###  Install Dependencies

pip install -r requirements.txt

### Apply Migrations

python manage.py migrate

## Load inintal Data

2. python manage.py loaddata data.json

### Create Superuser (Optional)

python manage.py createsuperuser

### Run Development Server

python manage.py runserver

Now open:
http://127.0.0.1:8000/
