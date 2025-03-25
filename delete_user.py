from app import create_app, db
from app.models import User

app = create_app()

def delete_user(username):
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            print(f"User {username} deleted successfully.")
        else:
            print(f"No user found with username: {username}")

if __name__ == '__main__':
    username_to_delete = input("Enter the username of the user to delete: ")
    delete_user(username_to_delete)
