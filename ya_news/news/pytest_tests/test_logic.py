from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertFormError

from news.models import Comment
from news.forms import BAD_WORDS, WARNING
from news.pytest_tests.constants import FORM_DATA, LOGIN_URL


def test_user_can_create_comment(
    author_client, author, news
):
    url = reverse('news:detail', args=(news.pk,))
    response = author_client.post(url, data=FORM_DATA)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.news == news
    assert new_comment.author == author
    assert new_comment.text == FORM_DATA['text']


def test_anonymous_user_cant_create_comment(
    client, news
):
    url = reverse('news:detail', args=(news.pk,))
    response = client.post(url, data=FORM_DATA)
    expected_url = f'{LOGIN_URL}?next={url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


def test_user_cant_use_bad_words(
    author_client, author, news
):
    url = reverse('news:detail', args=(news.pk,))
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING,
    )
    assert Comment.objects.count() == 0


def test_author_can_edit_comment(
    author_client, news, author, comment
):
    url = reverse('news:edit', args=(comment.pk,))
    news_url = reverse('news:detail', args=(news.pk,))
    response = author_client.post(url, FORM_DATA)
    assertRedirects(response, f'{news_url}#comments')
    comment.refresh_from_db()
    assert comment.news == news
    assert comment.author == author
    assert comment.text == FORM_DATA['text']


def test_another_user_cant_edit_comment(
    admin_client, comment
):
    url = reverse('news:edit', args=(comment.pk,))
    response = admin_client.post(url, FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(pk=comment.pk)
    assert comment.news == comment_from_db.news
    assert comment.author == comment_from_db.author
    assert comment.text == comment_from_db.text


def test_author_can_delete_comment(
    author_client, news, comment,
):
    url = reverse('news:delete', args=(comment.pk,))
    news_url = reverse('news:detail', args=(news.pk,))
    response = author_client.post(url)
    assertRedirects(response, f'{news_url}#comments')
    assert Comment.objects.count() == 0


def test_another_user_cant_delete_comment(
    admin_client, comment
):
    url = reverse('news:delete', args=(comment.pk,))
    db_befor_try_to_change = Comment.objects.all()
    response = admin_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    db_after_try_to_change = Comment.objects.all()
    assert db_befor_try_to_change, db_after_try_to_change
