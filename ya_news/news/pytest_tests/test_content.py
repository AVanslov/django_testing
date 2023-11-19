from django.urls import reverse

from news.forms import CommentForm
from news.pytest_tests.constants import HOME_URL
from yanews import settings


def test_news_count(many_news, client):
    assert len(
        client
        .get(HOME_URL)
        .context['object_list']
    ) == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(many_news, client):
    response = client.get(HOME_URL)
    all_dates = [
        news.date for news in response.context[
            'object_list'
        ]
    ]
    assert all_dates == sorted(all_dates, reverse=True)


def test_comments_order(client, news, many_comments):
    url = reverse('news:detail', args=(news.pk,))
    response = client.get(url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments_dates = [
        comment.created for comment in news
        .comment_set.filter(news=news)
    ]
    assert all_comments_dates == sorted(all_comments_dates, reverse=False)


def test_form_in_context_for_anonymnous_users(
    client, news
):
    url = reverse('news:detail', args=(news.pk,))
    assert 'form' not in client.get(url).context


def test_form_in_context_for_author(
    author_client, news
):
    url = reverse('news:detail', args=(news.pk,))
    response = author_client.get(url)
    assert 'form' in response.context
    form = response.context['form']
    assert isinstance(form, CommentForm)
