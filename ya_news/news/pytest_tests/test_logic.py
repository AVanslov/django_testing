from http import HTTPStatus

from pytest_django.asserts import (
    assertRedirects, assertFormError, assertQuerysetEqual
)

from news.models import Comment
from news.forms import WARNING
from news.pytest_tests.constants import BAD_WARDS_DATA, FORM_DATA


def test_user_can_create_comment(
    author_client, author, news, news_detail_url
):
    response = author_client.post(news_detail_url, data=FORM_DATA)
    assertRedirects(response, f'{news_detail_url}#comments')
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.news == news
    assert new_comment.author == author
    assert new_comment.text == FORM_DATA['text']


def test_anonymous_user_cant_create_comment(
    client, news, news_detail_url, comment_success_after_detail_url
):
    response = client.post(news_detail_url, data=FORM_DATA)
    assertRedirects(response, comment_success_after_detail_url)
    assert Comment.objects.count() == 0


def test_user_cant_use_bad_words(
    author_client, news_detail_url
):
    response = author_client.post(news_detail_url, data=BAD_WARDS_DATA)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING,
    )
    assert Comment.objects.count() == 0


def test_author_can_edit_comment(
    author_client, news, author, comment, comment_edit_url, news_detail_url
):
    response = author_client.post(comment_edit_url, FORM_DATA)
    assertRedirects(response, f'{news_detail_url}#comments')
    comment.refresh_from_db()
    assert comment.news == news
    assert comment.author == author
    assert comment.text == FORM_DATA['text']


def test_another_user_cant_edit_comment(
    admin_client, comment, comment_edit_url
):
    response = admin_client.post(comment_edit_url, FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(pk=comment.pk)
    assert comment.news == comment_from_db.news
    assert comment.author == comment_from_db.author
    assert comment.text == comment_from_db.text


def test_author_can_delete_comment(
    author_client, news_detail_url, comment_delete_url
):
    response = author_client.post(comment_delete_url)
    assertRedirects(response, f'{news_detail_url}#comments')
    assert Comment.objects.count() == 0


def test_another_user_cant_delete_comment(
    admin_client, comment_delete_url
):
    db_befor_try_to_change = Comment.objects.all()
    response = admin_client.post(comment_delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    db_after_try_to_change = Comment.objects.all()
    assertQuerysetEqual(db_befor_try_to_change, db_after_try_to_change)
