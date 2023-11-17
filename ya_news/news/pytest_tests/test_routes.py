from http import HTTPStatus

from django.urls import reverse
import pytest
from pytest_django.asserts import assertRedirects

AUTHOR = pytest.lazy_fixture('author_client')
ADMIN = pytest.lazy_fixture('admin_client')
ANONYMNOUS_USER = pytest.lazy_fixture('client')
PK_OF_COMMENT = pytest.lazy_fixture('pk_for_comment_args')
PK_OF_NEWS = pytest.lazy_fixture('pk_for_news_args')


@pytest.mark.parametrize(
    'url, args, parametrized_client, expected_status',
    (
        ('news:home', None, ANONYMNOUS_USER, HTTPStatus.OK),
        ('users:login', None, ANONYMNOUS_USER, HTTPStatus.OK),
        ('users:logout', None, ANONYMNOUS_USER, HTTPStatus.OK),
        ('users:signup', None, ANONYMNOUS_USER, HTTPStatus.OK),
        ('news:detail', PK_OF_NEWS, ANONYMNOUS_USER, HTTPStatus.OK),
        ('news:edit', PK_OF_COMMENT, AUTHOR, HTTPStatus.OK),
        ('news:delete', PK_OF_COMMENT, AUTHOR, HTTPStatus.OK),
        ('news:edit', PK_OF_COMMENT, ADMIN, HTTPStatus.NOT_FOUND),
        ('news:delete', PK_OF_COMMENT, ADMIN, HTTPStatus.NOT_FOUND),
    ),
)
def test_pages_return_code(
    url, args, parametrized_client, expected_status
):
    url = reverse(url, args=args)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:edit', PK_OF_COMMENT),
        ('news:delete', PK_OF_COMMENT),
    ),
)
def test_redirects(client, name, args):
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
