from django.test import SimpleTestCase, RequestFactory
from unittest.mock import patch, MagicMock
from django.contrib.messages.storage.fallback import FallbackStorage

from .views import user_login_view, user_logout_view


def new_mock_get_request(user, *args, **kwargs):
    req = RequestFactory().get(*args, **kwargs)
    setattr(req, 'user', user)
    setattr(req, 'session', {})
    setattr(req, '_messages', FallbackStorage(req))
    return req

def new_mock_post_request(user, *args, **kwargs):
    req = RequestFactory().post(*args, **kwargs)
    setattr(req, 'user', user)
    setattr(req, 'session', {})
    setattr(req, '_messages', FallbackStorage(req))
    return req


class UserLoginViewTestCase(SimpleTestCase):
    @patch('account.views.login')
    @patch('account.views.authenticate')
    def test_user_login_view(self, mock_authenticate_func, mock_login_func):
        # mock user
        mock_user = MagicMock()
        mock_user.is_authenticated = False

        mock_authenticate_func.return_value = mock_user

        # mock the post request
        req = new_mock_post_request(mock_user, '/account/login/', data={
            'username': 'cokecola',
            'password': '123456789'
        })

        resp = user_login_view(req)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/application/')

        # assert the repository methods were called
        mock_login_func.assert_called_once_with(req, mock_user)
