# Import the application objects from ``__init__`` instead of ``app`` to prevent
# this script from importing itself when run directly.
from __init__ import create_app, db
from models import User

app = create_app()

def list_users():
    with app.app_context():
        users = User.query.all()
        for user in users:
            print(f"Username: {user.username}, Email: {user.email}")

if __name__ == '__main__':
    list_users()
