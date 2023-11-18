from datetime import datetime, timedelta
from django.test import Client
from django.urls import reverse
import pytest

from news.models import News, Comment
from yanews import settings

COMMENTS_COUNT = 10


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(
    db,
):
    pass


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author):
    author_client = Client()
    author_client.force_login(author)
    return author_client


@pytest.fixture
def news():
    return News.objects.create(
        title='Загаловок',
        text='Содержимое новости',
    )


@pytest.fixture
def news_detail_url(news):
    return reverse('news:detail', args=(news.pk,))


@pytest.fixture
def many_news():
    today = datetime.today()
    return News.objects.bulk_create(
        [
            News(
                title=f'Новость {index}',
                text='Просто текст.',
                date=today - timedelta(days=index)
            )
            for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
        ]
    )


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )


@pytest.fixture
def comment_edit_url(comment):
    return reverse('news:edit', args=(comment.pk,))


@pytest.fixture
def comment_delete_url(comment):
    return reverse('news:delete', args=(comment.pk,))


@pytest.fixture
def many_comments(news, author):
    today = datetime.today()
    for index in range(COMMENTS_COUNT):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Просто текст.{index}',
        )
        comment.created = today - timedelta(days=index)
        comment.save()
