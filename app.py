# Import the application factory and mail instance from the package's
# ``__init__`` module instead of importing from ``app``. Importing from ``app``
# causes this module to import itself, leading to a circular import error when
# executing scripts directly.
from __init__ import create_app, mail
from flask_mail import Message

app = create_app()

@app.route('/test-email')
def test_email():
    try:
        msg = Message('Test Email', sender='rovicr@gmail.com', recipients=['rovicr@outlook.com'])
        msg.body = 'This is a test email.'
        mail.send(msg)
        return 'Test email sent successfully!'
    except Exception as e:
        return f'Error sending test email: {e}'

if __name__ == '__main__':
    app.run(debug=True)
