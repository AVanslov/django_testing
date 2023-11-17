from django.urls import reverse
import pytest

from yanews import settings


@pytest.mark.django_db
def test_news_count(many_news, client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(many_news, client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates, sorted_dates


@pytest.mark.django_db
def test_comments_order(client, news, many_comments):
    url = reverse('news:detail', args=(news.pk,))
    response = client.get(url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.parametrize(
    'parametrized_client, form_in_context',
    (
        (pytest.lazy_fixture('client'), False),
        (pytest.lazy_fixture('author_client'), True),
    )
)
@pytest.mark.django_db
def test_form_in_context_for_different_users(
    parametrized_client, form_in_context, news, pk_for_news_args
):
    url = reverse('news:detail', args=pk_for_news_args)
    response = parametrized_client.get(url)
    assert ('form' in response.context) is form_in_context
