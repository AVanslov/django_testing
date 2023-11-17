from datetime import datetime, timedelta
import pytest

from news.models import News, Comment
from yanews import settings

COMMENTS_COUNT = 10


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Загаловок',
        text='Содержимое новости',
    )
    return news


@pytest.fixture
def pk_for_news_args(news):
    return news.pk,


@pytest.fixture
def many_news():
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)
    return all_news


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )
    return comment


@pytest.fixture
def pk_for_comment_args(comment):
    return comment.pk,


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
    return comment


@pytest.fixture
def form_data():
    return {
        'text': 'Комментарий',
    }
