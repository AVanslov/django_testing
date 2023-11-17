from http import HTTPStatus
import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from django.urls import reverse
from news.forms import BAD_WORDS, WARNING

from news.models import Comment


def test_user_can_create_comment(
    author_client, author, news, form_data, pk_for_news_args
):
    url = reverse('news:detail', args=pk_for_news_args)
    response = author_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.text == form_data['text']
    assert new_comment.author == author


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
    client, form_data, news, pk_for_news_args
):
    url = reverse('news:detail', args=pk_for_news_args)
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


def test_user_cant_use_bad_words(
    author_client, author, news, form_data, pk_for_news_args
):
    url = reverse('news:detail', args=pk_for_news_args)
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
    author_client, form_data, pk_for_comment_args, comment, pk_for_news_args
):
    url = reverse('news:edit', args=pk_for_comment_args)
    news_url = reverse('news:detail', args=pk_for_news_args)
    response = author_client.post(url, form_data)
    assertRedirects(response, f'{news_url}#comments')
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_another_user_cant_edit_comment(
    admin_client, form_data, pk_for_comment_args, comment, pk_for_news_args
):
    url = reverse('news:edit', args=pk_for_comment_args)
    response = admin_client.post(url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(pk=comment.pk)
    assert comment.text == comment_from_db.text


def test_author_can_delete_comment(
    author_client, pk_for_comment_args, pk_for_news_args,
):
    url = reverse('news:delete', args=pk_for_comment_args)
    news_url = reverse('news:detail', args=pk_for_news_args)
    response = author_client.post(url)
    assertRedirects(response, f'{news_url}#comments')
    assert Comment.objects.count() == 0


def test_another_user_cant_delete_comment(
    admin_client, form_data, pk_for_comment_args,
):
    url = reverse('news:delete', args=pk_for_comment_args)
    response = admin_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
