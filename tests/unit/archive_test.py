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
        # Create 2 users
        u1 = User(username='jackson1')
        u2 = User(username='jackson2')
        db.session.add(u1)
        db.session.add(u2)

        # Create a post for u1
        now = datetime.utcnow()
        time = now.strftime("%Y-%m-%d %H:%M:%S.%f")
        post_j1= Post(body="testing archive feature", author=u1, timestamp=now + timedelta(seconds=1))
        db.session.add(post_j1)
        db.session.commit()

        # As u2, archive u1's posts
        u2.archive(post_id=post_j1.id, post_body=post_j1.body, post_user=u1.username, user_id=u1.id, post_time=time)
        db.session.commit()
        self.assertTrue(u2.has_archived_post(post_j1.id))
        self.assertEqual(u2.archived.count(), 1)
        self.assertEqual(u2.archived.first().body, "testing archive feature")

        # As u2, remove the post from your archive
        u2.archive_remove(post_id=post_j1.id)
        db.session.commit()
        self.assertFalse(u2.has_archived_post(post_j1.id))
        self.assertEqual(u2.archived.count(), 0)

    def test_archive_post_original_deleted(self):
        # Create 2 users
        u1 = User(username='jackson1')
        u2 = User(username='jackson2')
        db.session.add(u1)
        db.session.add(u2)

        # Create a post for u1
        now = datetime.utcnow()
        time = now.strftime("%Y-%m-%d %H:%M:%S.%f")
        post_j1= Post(body="testing archive feature", author=u1, timestamp=now + timedelta(seconds=1))
        db.session.add(post_j1)
        db.session.commit()

        # As u2, archive u1's posts
        u2.archive(post_id=post_j1.id, post_body=post_j1.body, post_user=u1.username, user_id=u1.id, post_time=time)
        db.session.commit()
        self.assertTrue(u2.has_archived_post(post_j1.id))
        self.assertEqual(u2.archived.count(), 1)
        self.assertEqual(u2.archived.first().body, "testing archive feature")

        # As u1, delete your post
        u1.delete_post(post_id=post_j1.id)
        db.session.commit()
        self.assertEqual(u2.posts.count(), 0)
        
        # Check to make sure post was not deleted from u2's archive
        self.assertTrue(u2.has_archived_post(post_j1.id))
        self.assertEqual(u2.archived.count(), 1)
        self.assertEqual(u2.archived.first().body, "testing archive feature")

        # As u2, remove the post from your archive
        u2.archive_remove(post_id=post_j1.id)
        db.session.commit()
        self.assertFalse(u2.has_archived_post(post_j1.id))
        self.assertEqual(u2.archived.count(), 0)    


if __name__ == '__main__':
    unittest.main()