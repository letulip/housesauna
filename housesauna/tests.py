import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .views import IndexView
from houses.models import House, Sauna

def create_structure(structure_type, short_name, images_count, days):
    """
    Create a structure with a given 'short_name' and published the given number of 'days' offset to now (negative for structures published in the past, positive for structures that have yet to be published)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    type = House if structure_type == 'House' else Sauna
    return type.objects.create(
        short_name=short_name,
        images_count=images_count,
        pub_date=time
    )

class IndexViewTests(TestCase):
    def test_no_structures(self):
        """
        If no structures exist, an appropriate message is displayed.
        """
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'No structures are available.')
        self.assertQuerysetEqual(resp.context['recent_projects'], [])

    def test_past_structures(self):
        """
        Structures with a pub_date in the past are displayed on the index page.
        """
        house = create_structure('House', 'small-house-30', 1, -30)
        sauna = create_structure('Sauna', 'small-sauna-30', 1, -30)
        resp = self.client.get('/')
        self.assertQuerysetEqual(
            resp.context['recent_projects'],
            [house, sauna]
        )

    def test_future_structure(self):
        """
        Structure with a pub_date in the future aren't displayed on the index page.
        """
        create_structure('House', 'small-house-30', 1, 30)
        create_structure('Sauna', 'small-sauna-30', 1, 30)
        resp = self.client.get('/')
        self.assertContains(resp, 'No structures are available.')
        self.assertQuerysetEqual(resp.context['recent_projects'], [])

    def test_future_structure_and_past_structure(self):
        """
        Even if both past and future structures exist, only past structures are displayed.
        """
        house = create_structure('House', 'small-house-30', 1, -30)
        create_structure('Sauna', 'small-sauna-31', 1, 30)
        resp = self.client.get('/')
        self.assertQuerysetEqual(
            resp.context['recent_projects'],
            [house]
        )

    def test_two_past_structures(self):
        """
        The structures index page may display multiple structures.
        """
        house = create_structure('House', 'small-house-30', 1, -30)
        sauna = create_structure('Sauna', 'small-sauna-30', 1, -5)
        resp = self.client.get('/')
        self.assertQuerysetEqual(
            resp.context['recent_projects'],
            [house, sauna]
        )

class StructureDetailViewTests(TestCase):
    def test_future_structure(self):
        """
        The detail view of a structure with a pub_date in the future returns a 404 not found.
        """
        future_house = create_structure('House', 'small-house-30', 1, 5)
        future_sauna = create_structure('Sauna', 'small-sauna-30', 1, 5)
        url = reverse('houses:detail', args=(future_house.id,))
        url1 = reverse('houses:detail', args=(future_sauna.id,))
        resp = self.client.get(url)
        resp1 = self.client.get(url1)
        # self.assertEqual(resp.status_code, 404)
        # self.assertEqual(resp1.status_code, 404)
        self.assertContains(resp, 'Страница не найдена')
        self.assertContains(resp1, 'Страница не найдена')

    def test_past_structure(self):
        """
        The detail view of a structure with a pub_date in the past displays the question's text.
        """
        past_house = create_structure('House', 'small-house-30', 1, -5)
        past_sauna = create_structure('Sauna', 'small-sauna-30', 1, -5)
        url = reverse('houses:detail', args=(past_house.id,))
        url1 = reverse('houses:detail', args=(past_sauna.id,))
        resp = self.client.get(url)
        resp1 = self.client.get(url1)
        self.assertContains(resp, past_house.full_name)
        self.assertContains(resp1, past_sauna.full_name)