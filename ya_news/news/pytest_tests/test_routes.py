from http import HTTPStatus

from pytest_django.asserts import assertRedirects
from django.urls import reverse
import pytest


@pytest.mark.parametrize(
    'name',
    ('news:home', 'users:login', 'users:logout', 'users:signup'),
)
def test_users_pages_availability_for_anonymous_user(db, client, name):
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    ('news:detail',),
)
def test_news_detail_page_availabilyty_for_anonymous_user(
    db, client, name, pk_for_news_args
):
    url = reverse(name, args=(pk_for_news_args))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND),
    )
)
@pytest.mark.parametrize(
    'name',
    (
        'news:edit',
        'news:delete',
    ),
)
def test_pages_availability_for_author(
    parametrized_client, name, comment, expected_status, pk_for_comment_args
):
    url = reverse(name, args=pk_for_comment_args)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:edit', pytest.lazy_fixture('pk_for_comment_args')),
        ('news:delete', pytest.lazy_fixture('pk_for_comment_args')),
    ),
)
def test_redirects(db, client, name, args):
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
