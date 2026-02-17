Clone the repository:

    git clone https://github.com/yourusername/QuizZone.git
    cd QuizZone

Create a virtual environment:

    python -m venv venv
    source venv/bin/activate   # Linux/macOS
    venv\Scripts\activate      # Windows


Install dependencies:

    pip install -r requirements.txt


Apply migrations:

    python manage.py migrate


Create a superuser (optional, for admin):

    python manage.py createsuperuser


Run the server:

    python manage.py runserver