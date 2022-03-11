from django.test import TestCase
from django.contrib.auth.models import User

class SignUpTestCase(TestCase):
    def setUp(self) -> None:
        usr = User.objects.create_user("12thMan", "twelve@testtamu.edu", "SomePassword123")
        usr.first_name = "12th"
        usr.last_name = "Man"
        usr.save()

    def test_successful_signup(self):
        user_data = {
            "username": "acoolsomebody",
            "password": "CoolFolks12345!",
            "first_name": "Jon",
            "last_name": "Doe",
            "email": "jondoe@yahoo.com"
        }

        expected_out = {
            "created": "success"
        }

        resp = self.client.post('/auth/signup/', data=user_data)

        self.assertEqual(resp.data, expected_out)


    def test_duplicate_signup_username(self):
        user_data = {
            "username": "12thMan",
            "password": "CoolFolks12345!",
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "janedoe@email.com"
        }

        expected_out = {
            "created": "username exists"
        }

        resp = self.client.post('/auth/signup/', data=user_data)
        self.assertEqual(resp.data, expected_out)

    def test_duplicate_signup_email(self):
        user_data = {
            "username": "13thMan",
            "password": "CoolFolks12345!",
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "twelve@testtamu.edu"
        }

        expected_out = {
            "created": "email exists"
        }

        resp = self.client.post('/auth/signup/', data=user_data)
        self.assertEqual(resp.data, expected_out)

