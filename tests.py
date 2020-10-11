import os
import unittest
 
from app import app, db

class BasicTests(unittest.TestCase):
    def setUp(self):
        app.config.from_object(os.environ.get('FLASK_ENV') or 'config.TestingConfig')
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
 
    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()
 
 
###############
#### tests ####
###############
 
    def test_login_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_correct_user_login(self):
        response = self.app.post(
        '/',
        data=dict(email='test@innopolis.com', password='password_test'),
        follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello test', response.data)

    def test_wrong_user_login(self):
        response = self.app.post(
        '/',
        data=dict(email='test@testing.com', password='password_test'),
        follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign In', response.data)

    def test_regitered_user(self):
        self.app.post(
        '/',
        data=dict(email='test@innopolis.com', password='password_test'),
        follow_redirects=True)
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello test', response.data)

if __name__ == "__main__":
    unittest.main()