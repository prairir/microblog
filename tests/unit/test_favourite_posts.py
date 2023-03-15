import sys
import os

from flask import url_for

newPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))
sys.path.append(newPath)

from app.main.routes import archive
from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import Post, User, Archive
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ELASTICSEARCH_URL = None

class EditPostTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_archived_posts_url(self):
        u = User(username='manraj')
        with self.app.app_context(), self.app.test_request_context():
            self.assertEqual('/archived/' + u.username, url_for('main.view_archive', username=u.username))
    
    def test_archive_post(self):
        u = User(username='manraj')
        now = datetime.utcnow()
        p = Post(body="post from manraj", author=u,
                  timestamp=now + timedelta(seconds=1))
        
        a = u.archive(p.id, p.body, u.id, p.author, str(p.timestamp))
        
        self.assertEqual(a, True)


if __name__ == '__main__':
    unittest.main()