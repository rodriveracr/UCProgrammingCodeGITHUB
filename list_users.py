from app import create_app, db
from app.models import User

app = create_app()

def list_users():
    with app.app_context():
        users = User.query.all()
        for user in users:
            print(f"Username: {user.username}, Email: {user.email}")

if __name__ == '__main__':
    list_users()
