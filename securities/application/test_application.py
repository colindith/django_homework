from django.test import SimpleTestCase, RequestFactory
from unittest.mock import patch, MagicMock
from django.contrib.messages.storage.fallback import FallbackStorage

from .views import apply_view, status_view, update_application_view


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


class ApplyViewTestCase(SimpleTestCase):
    @patch('application.views.Repository')
    @patch('application.views.ApplicationForm')
    def test_apply_view(self, mock_application_form, mock_repository_class):
        # mock appication model and form object
        mock_repo_inst = MagicMock()
        mock_form = MagicMock()
        mock_application_model = MagicMock()
        mock_repo_inst.get_application_by_user.return_value = None
        mock_form.save.return_value = mock_application_model

        mock_repository_class.return_value = mock_repo_inst
        mock_application_form.return_value = mock_form

        # mock user
        mock_user = MagicMock()
        mock_user.is_authenticated = True

        # mock the post request
        req = new_mock_post_request(mock_user, '/application/', data={
            'account_name': 'dylan',
            'phone_number': '12345678',
            'address': 'No.1, City Hall Rd., Xinyi District, Taipei City'
        })

        resp = apply_view(req)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/application/status/')

        # assert the repository methods were called
        mock_repo_inst.get_application_by_user.assert_called_once_with(mock_user)
        mock_repo_inst.save_application_and_update_status.assert_called_once_with(mock_form, mock_user, 'PENDING')


class StatusViewTestCase(SimpleTestCase):
    @patch('application.views.Repository')
    @patch('application.views.messages')
    def test_status_view_pending(self, mock_message, mock_repository_class):
        # mock appication model and form object
        mock_repo_inst = MagicMock()
        mock_application_model = MagicMock()
        mock_application_model.status = 'PENDING'
        mock_repo_inst.get_application_by_user.return_value = mock_application_model

        mock_repository_class.return_value = mock_repo_inst

        # mock user
        mock_user = MagicMock()
        mock_user.is_authenticated = True

        # mock the get request
        req = new_mock_get_request(mock_user,'/application/status/')

        resp = status_view(req)

        self.assertEqual(resp.status_code, 200)

        # assert the repository methods were called
        mock_repo_inst.get_application_by_user.assert_called_once_with(mock_user, raise_404_if_not_exist=True)

        # assert message
        mock_message.success.assert_called_with(req, 'Your application is currently under review.')

    @patch('application.views.Repository')
    @patch('application.views.messages')
    def test_status_view_approved(self, mock_message, mock_repository_class):
        # mock appication model and form object
        mock_repo_inst = MagicMock()
        mock_application_model = MagicMock()
        mock_application_model.status = 'APPROVED'
        mock_repo_inst.get_application_by_user.return_value = mock_application_model

        mock_repository_class.return_value = mock_repo_inst

        # mock user
        mock_user = MagicMock()
        mock_user.is_authenticated = True

        # mock the get request
        req = new_mock_get_request(mock_user,'/application/status/')

        resp = status_view(req)

        self.assertEqual(resp.status_code, 200)

        # assert the repository methods were called
        mock_repo_inst.get_application_by_user.assert_called_once_with(mock_user, raise_404_if_not_exist=True)

        # assert message
        mock_message.success.assert_called_with(req, 'Congratulation! Your application has been approved.')

    @patch('application.views.Repository')
    @patch('application.views.messages')
    def test_status_view_rejected(self, mock_message, mock_repository_class):
        # mock appication model and form object
        mock_repo_inst = MagicMock()
        mock_application_model = MagicMock()
        mock_application_model.status = 'REJECTED'
        mock_application_model.reason = 'incorrect phone number'
        mock_repo_inst.get_application_by_user.return_value = mock_application_model

        mock_repository_class.return_value = mock_repo_inst

        # mock user
        mock_user = MagicMock()
        mock_user.is_authenticated = True

        # mock the get request
        req = new_mock_get_request(mock_user,'/application/status/')

        resp = status_view(req)

        self.assertEqual(resp.status_code, 200)

        # assert the repository methods were called
        mock_repo_inst.get_application_by_user.assert_called_once_with(mock_user, raise_404_if_not_exist=True)

        # assert message
        mock_message.info.assert_called_with(req, 'The application has been rejected. Reason: incorrect phone number')

    @patch('application.views.Repository')
    @patch('application.views.messages')
    def test_status_view_missing_document(self, mock_message, mock_repository_class):
        # mock appication model and form object
        mock_repo_inst = MagicMock()
        mock_application_model = MagicMock()
        mock_application_model.status = 'MISSING_DOCUMENTS'
        mock_application_model.reason = 'incorrect phone number'
        mock_repo_inst.get_application_by_user.return_value = mock_application_model

        mock_repository_class.return_value = mock_repo_inst

        # mock user
        mock_user = MagicMock()
        mock_user.is_authenticated = True

        # mock the get request
        req = new_mock_get_request(mock_user,'/application/status/')

        resp = status_view(req)

        self.assertEqual(resp.status_code, 200)

        # assert the repository methods were called
        mock_repo_inst.get_application_by_user.assert_called_once_with(mock_user, raise_404_if_not_exist=True)

        # assert message
        mock_message.info.assert_called_with(req, 'The application is missing some necessary information. Reason: incorrect phone number')


class UpdateApplicationViewTestCase(SimpleTestCase):
    @patch('application.views.Repository')
    @patch('application.views.ApplicationForm')
    def test_update_application_view(self, mock_application_form, mock_repository_class):
        # mock appication model and form object
        mock_repo_inst = MagicMock()
        mock_form = MagicMock()
        mock_application_model = MagicMock()
        mock_repo_inst.get_application_by_user.return_value = mock_application_model
        mock_form.save.return_value = mock_application_model

        mock_repository_class.return_value = mock_repo_inst
        mock_application_form.return_value = mock_form

        # mock user
        mock_user = MagicMock()
        mock_user.is_authenticated = True

        # mock the post request
        req = new_mock_post_request(mock_user,'/application/update', data={
            'account_name': 'dylan',
            'phone_number': '12345678',
            'address': 'No.1, City Hall Rd., Xinyi District, Taipei City'
        })

        resp = update_application_view(req)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/application/status/')

        # assert the repository methods were called
        mock_repo_inst.get_application_by_user.assert_called_once_with(mock_user, status='MISSING_DOCUMENTS', raise_404_if_not_exist=True)
        mock_repo_inst.save_application_and_update_status.assert_called_once_with(mock_form, mock_user, 'PENDING')
