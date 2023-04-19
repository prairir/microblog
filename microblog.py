# Import necessary modules from the app package
from app import create_app, db, cli
from app.models import User, Post, Message, Notification, Task

# Create a Flask app instance by calling create_app() function
app = create_app()

# Register the CLI commands with the app instance
cli.register(app)

# Define a shell context processor to add app instance and database models to the Flask shell context


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Message': Message,
            'Notification': Notification, 'Task': Task}
