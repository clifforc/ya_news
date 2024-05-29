import pytest

from django.urls import reverse

from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_count(client, setup_home_page_data):
    home_url = reverse('news:home')
    response = client.get(home_url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, setup_home_page_data):
    home_url = reverse('news:home')
    response = client.get(home_url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comments_order(client, setup_detail_page_data, news):
    detail_url = reverse("news:detail", args=(news.id,))
    response = client.get(detail_url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.parametrize(
    'parametrized_client, expected_form',
    (
        (pytest.lazy_fixture('client'), False),
        (pytest.lazy_fixture('author_client'), True)
    ),
)
@pytest.mark.django_db
def test_form_availability_for_different_users(
        news, parametrized_client, expected_form
):
    url = reverse('news:detail', args=(news.id,))
    response = parametrized_client.get(url)
    assert ('form' in response.context) is expected_form
