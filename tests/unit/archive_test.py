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

class ArchivePostTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_archive_post(self):
        u1 = User(username='jackson1')
        u2 = User(username='jackson2')

        db.session.add(u1)
        db.session.add(u2)

        time = datetime.utcnow()
        post_j1= Post(body="testing archive feature", author=u1, timestamp=time + timedelta(seconds=1))

        db.session.add(post_j1)
        db.session.commit()

        u2.archive(post_id=post_j1.id, post_body=post_j1.body, post_user=u1.username, user_id=u1.id, post_time=post_j1.timestamp)
        db.session.commit()
        self.assertTrue(u2.has_archived_post(post_j1.id))
        self.assertEqual(u2.archived.count(), 1)
        self.assertEqual(u2.archived.first().body, "testing archive feature")

        u2.archive_remove(post_id=post_j1.id)
        db.session.commit()
        self.assertFalse(u2.has_archived_post(post_j1.id))
        self.assertEqual(u2.archived.count(), 0)


