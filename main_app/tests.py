from django.test import TestCase
from unittest.mock import Mock

from main_app.view_classes.signup import SignupView


# Create your tests here.
class TestSignup(TestCase):

    def test_sign_up_with_existing_email(self):
        request1 = Mock()
        request1.data = {
                'email': 'test1@email.com',
                'password': 'justinluu8235'
            }

        request2 = Mock()
        request2.data = {
                'email': 'test1@email.com',
                'password': 'justinlee8235'
            }

        response1 = SignupView().sign_up(request1)
        print(response1)
        assert response1.data['email'] == 'test1@email.com'
        assert response1.data['id'] == 1

        response2 = SignupView().sign_up(request2)
        assert response2.data['errors'] == 'A user with that email already exists. \n'

