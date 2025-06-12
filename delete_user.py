# Import application objects from ``__init__`` instead of ``app`` to avoid
# importing this script as a module, which leads to circular imports when the
# script is executed directly.
from __init__ import create_app, db
from models import User

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
