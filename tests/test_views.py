import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from houses.models import House, Sauna, Project, Category


@pytest.mark.django_db
def test_index_view_shows_only_published_projects(client):
    '''IndexView отображает только проекты с pub_date в прошлом или настоящем.'''
    Project.objects.create(
        full_name='project-a',
        slug='p-a',
        short_name='pa',
        title='Проект A',
        dimensions='10x10',
        square=100,
        image='fake.jpg',
        pub_date=timezone.now() - timedelta(days=1)
    )
    Project.objects.create(
        full_name='future-project',
        slug='fp',
        short_name='fp',
        title='Будущий проект',
        dimensions='10x10',
        square=100,
        image='future.jpg',
        pub_date=timezone.now() + timedelta(days=10)
    )
    url = reverse('houses:index')
    response = client.get(url)
    assert response.status_code == 200
    content = response.content.decode()
    assert 'Проект A' in content
    assert 'Будущий проект' not in content


@pytest.mark.django_db
def test_project_detail_view_accessible_by_full_name(client):
    '''ProjectDetailView отображает проект по full_name (используется в URL как slug).'''
    project = Project.objects.create(
        full_name='project-x',
        slug='px',
        short_name='px',
        title='Проект X',
        dimensions='9x9',
        square=90,
        image='x.jpg',
        pub_date=timezone.now()
    )
    url = reverse('houses:project-detail', kwargs={'slug': project.full_name})
    response = client.get(url)
    assert response.status_code == 200
    assert 'Проект X' in response.content.decode()


@pytest.mark.django_db
def test_category_sauna_view_filters_categories(client, settings):
    '''CategorySaunaView показывает только категории, где есть связанные бани.'''
    cat_with_sauna = Category.objects.create(name='Сауны', slug='saunas')
    cat_empty = Category.objects.create(name='Без бань', slug='none')
    sauna = Sauna.objects.create(
        full_name='sauna-1',
        slug='s1',
        short_name='s1',
        title='Баня',
        dimensions='8x8',
        square='64',
        cost='',
        video_url='',
        construction='',
        brus='',
        images_count=1,
        pub_date=timezone.now()
    )
    sauna.category.add(cat_with_sauna)

    settings.METATAGS = {'sauna': {'title': 'Сауны', 'description': 'Описание'}}

    url = reverse('houses:sauna_categories')
    response = client.get(url)
    content = response.content.decode()

    assert response.status_code == 200
    assert 'Сауны' in content
    assert 'Без бань' not in content
    assert 'Баня' in content
    assert 'Описание' in content


@pytest.mark.django_db
def test_category_houses_view_filters_categories(client, settings):
    '''CategoryHousesView отображает только категории, где есть связанные дома.'''
    cat_with_house = Category.objects.create(name='Дома', slug='houses')
    cat_empty = Category.objects.create(name='Пусто', slug='empty')

    house = House.objects.create(
        full_name='house-1',
        slug='h1',
        short_name='h1',
        title='Пример дома',
        dimensions='9x9',
        square='81',
        cost='6 000 000',
        video_url='',
        construction='2 мес',
        brus='Ш 150/ В 140',
        images_count=5,
        pub_date=timezone.now()
    )
    house.category.add(cat_with_house)

    settings.METATAGS = {'house': {'title': 'Тайтл для домов', 'description': 'Описание для домов'}}

    url = reverse('houses:houses_categories')
    response = client.get(url)
    content = response.content.decode()

    assert response.status_code == 200
    assert 'Дома' in content
    assert 'Пусто' not in content
    assert 'Пример дома' in content
    assert 'Описание для домов' in content


@pytest.mark.django_db
def test_subcategory_view_uses_json_descriptions(client):
    '''SubcategoriesHousesView берёт title/desc/header из subcategories_description, если они есть.'''
    parent = Category.objects.create(name='Категория', slug='cat')
    child = Category.objects.create(name='Подкатегория', slug='sub')
    parent.subcategory.add(child)

    parent.subcategories_description = {
        str(child.id): {
            'title': 'Тайтл из JSON',
            'description': 'Описание из JSON',
            'header': 'Хэдер из JSON'
        }
    }
    parent.save()

    house = House.objects.create(
        full_name='house-x',
        slug='hx',
        short_name='hx',
        title='Дом X',
        dimensions='10x10',
        square='100',
        cost='',
        video_url='',
        construction='',
        brus='',
        images_count=1,
        pub_date=timezone.now()
    )
    house.category.add(child)

    url = reverse('houses:houses_sub_list', kwargs={'cat_slug': parent.slug, 'sub_slug': child.slug})
    response = client.get(url)
    content = response.content.decode()

    assert response.status_code == 200
    assert 'Тайтл из JSON' in content
    assert 'Описание из JSON' in content
    assert 'Хэдер из JSON' in content
