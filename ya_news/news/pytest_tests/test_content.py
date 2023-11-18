from django.urls import reverse
from news.forms import CommentForm

from yanews import settings


def test_news_count(many_news, client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    assert len(object_list) == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(many_news, client):
    url = reverse('news:home')
    response = client.get(url)
    all_dates = [
        news.date for news in response.context[
            'object_list'
        ]
    ]
    assert all_dates, sorted(all_dates, reverse=True)


def test_comments_order(client, news, many_comments):
    url = reverse('news:detail', args=(news.pk,))
    response = client.get(url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    comments_created_at = [comment.created for comment in all_comments]
    assert sorted(comments_created_at), comments_created_at


def test_form_in_context_for_anonymnous_users(
    client, news
):
    url = reverse('news:detail', args=(news.pk,))
    response = client.get(url)
    assert 'form' not in response.context


def test_form_in_context_for_author(
    author_client, news
):
    url = reverse('news:detail', args=(news.pk,))
    response = author_client.get(url)
    assert isinstance('form', CommentForm) in response.context
