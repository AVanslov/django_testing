from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

from news.pytest_tests.constants import (
    ADMIN,
    ANONYMNOUS_USER,
    AUTHOR,
    COMMENT_DELETE_URL,
    COMMENT_EDIT_URL,
    EXPECTED_AFTER_DELETE_URL,
    EXPECTED_AFTER_EDIT_URL,
    HOME_URL,
    LOGIN_URL,
    LOGOUT_URL,
    NEWS_DETAIL_URL,
    SIGNUP_URL,
)


@pytest.mark.parametrize(
    'url, parametrized_client, expected_status',
    (
        (HOME_URL, ANONYMNOUS_USER, HTTPStatus.OK),
        (LOGIN_URL, ANONYMNOUS_USER, HTTPStatus.OK),
        (LOGOUT_URL, ANONYMNOUS_USER, HTTPStatus.OK),
        (SIGNUP_URL, ANONYMNOUS_USER, HTTPStatus.OK),
        (NEWS_DETAIL_URL, ANONYMNOUS_USER, HTTPStatus.OK),
        (COMMENT_EDIT_URL, AUTHOR, HTTPStatus.OK),
        (COMMENT_DELETE_URL, AUTHOR, HTTPStatus.OK),
        (COMMENT_EDIT_URL, ADMIN, HTTPStatus.NOT_FOUND),
        (COMMENT_DELETE_URL, ADMIN, HTTPStatus.NOT_FOUND),
    ),
)
def test_pages_return_code(
    url, parametrized_client, expected_status
):
    assert parametrized_client.get(url).status_code == expected_status


@pytest.mark.parametrize(
    'url, expected_url',
    (
        (COMMENT_EDIT_URL, EXPECTED_AFTER_EDIT_URL,),
        (COMMENT_DELETE_URL, EXPECTED_AFTER_DELETE_URL,),
    ),
)
def test_redirects(client, url, expected_url):
    assertRedirects(client.get(url), expected_url)
