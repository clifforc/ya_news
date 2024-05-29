import pytest

from datetime import timedelta

from django.utils import timezone
from django.test.client import Client
from django.contrib.auth import get_user_model

from yanews.settings import NEWS_COUNT_ON_HOME_PAGE
from news.models import News, Comment

User = get_user_model()


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news(author):
    news = News.objects.create(
        title='Тестовая новость',
        text='Просто текст.',
    )
    return news


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )
    return comment


@pytest.fixture
def id_for_args(news):
    return (news.id,)


@pytest.fixture
def id_comment_for_args(comment):
    return (comment.id,)


@pytest.fixture
def setup_home_page_data():
    for index in range(NEWS_COUNT_ON_HOME_PAGE + 1):
        news = News.objects.create(title=f'Новость {index}', text='Просто текст.')
        news.save()
    return index


@pytest.fixture
def setup_detail_page_data(author, news):
    now = timezone.now()
    comments = []
    for index in range(2):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f"Текст {index}",
        )
        comment.created = now + timedelta(days=index)
        comment.save()
        comments.append(comment)
    return comments


@pytest.fixture
def form_data():
    return {
        'title': 'Новый заголовок',
        'text': 'Новый текст'
    }
