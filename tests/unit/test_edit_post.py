import sys
import os
newPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))
sys.path.append(newPath)

from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import User, Post
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
    
    def test_edit_post(self):
        u = User(username='manraj')
        db.session.add(u)

        now = datetime.utcnow()
        p1 = Post(body="post from manraj", author=u,
                  timestamp=now + timedelta(seconds=1))
        db.session.add(p1)
        db.session.commit()

        p2 = Post(body="post from manraj but different", author=u,
                  timestamp=now + timedelta(seconds=1))
        p1 = p2
        db.session.add(p1)
        db.session.commit()

        self.assertEqual(p1, p2)


if __name__ == '__main__':
    unittest.main()