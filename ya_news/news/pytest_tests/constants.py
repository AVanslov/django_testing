from django.urls import reverse
import pytest

from news.forms import BAD_WORDS


AUTHOR = pytest.lazy_fixture('author_client')
ADMIN = pytest.lazy_fixture('admin_client')
ANONYMNOUS_USER = pytest.lazy_fixture('client')
NEWS_DETAIL_URL = pytest.lazy_fixture('news_detail_url')
COMMENT_EDIT_URL = pytest.lazy_fixture('comment_edit_url')
COMMENT_DELETE_URL = pytest.lazy_fixture('comment_delete_url')
HOME_URL = reverse('news:home')
LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
SIGNUP_URL = reverse('users:signup')
EXPECTED_AFTER_EDIT_URL = pytest.lazy_fixture(
    'comment_success_after_edit_url'
)
EXPECTED_AFTER_DELETE_URL = pytest.lazy_fixture(
    'comment_success_after_delete_url'
)
EXPECTED_AFTER_DETAIL_URL = pytest.lazy_fixture(
    'comment_success_after_detail_url'
)
FORM_DATA = {
    'text': 'Комментарий',
}
BAD_WARDS_DATA = {
    'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'
}
