import json
import sys
import time
from flask import render_template
from rq import get_current_job
from app import create_app, db
from app.models import User, Post, Task
from app.email import send_email

app = create_app()
app.app_context().push()


def _set_task_progress(progress):
    # Update the progress of the current job in the Redis queue
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()

        # Update the task progress in the database and send a notification to the user
        task = Task.query.get(job.get_id())
        task.user.add_notification('task_progress', {'task_id': job.get_id(),
                                                     'progress': progress})
        if progress >= 100:
            task.complete = True
        db.session.commit()


def export_posts(user_id):
    try:
        # Get the user by ID and start the progress at 0%
        user = User.query.get(user_id)
        _set_task_progress(0)
        data = []
        i = 0
        total_posts = user.posts.count()

        # Iterate over each post and append its body and timestamp to the data list
        for post in user.posts.order_by(Post.timestamp.asc()):
            data.append({'body': post.body,
                         'timestamp': post.timestamp.isoformat() + 'Z'})

            # Pause for 5 seconds and update the progress
            time.sleep(5)
            i += 1
            _set_task_progress(100 * i // total_posts)

        # Send an email with the exported posts as an attachment
        send_email('[Microblog] Your blog posts',
                   sender=app.config['ADMINS'][0], recipients=[user.email],
                   text_body=render_template(
                       'email/export_posts.txt', user=user),
                   html_body=render_template('email/export_posts.html',
                                             user=user),
                   attachments=[('posts.json', 'application/json',
                                 json.dumps({'posts': data}, indent=4))],
                   sync=True)
    except:
        # If an exception occurs, set the progress to 100% and log the error
        _set_task_progress(100)
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())
