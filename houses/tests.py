import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import House, Sauna

# Create your tests here.

class StructureModelTests(TestCase):

  def test_was_published_recently_with_future_structure(self):
    """
    was_published_recently() returns False for structures whose pub_date is in the future.
    """
    time = timezone.now() + datetime.timedelta(days=30)
    future_house = House(pub_date=time)
    future_sauna = Sauna(pub_date=time)
    self.assertIs(future_house.was_published_recently(), False)
    self.assertIs(future_sauna.was_published_recently(), False)

  def test_was_published_recently_with_old_structure(self):
    """
    was_published_recently() returns False for structures whose pub_date is older than 1 day.
    """
    time = timezone.now() - datetime.timedelta(days=1, seconds=1)
    old_house = House(pub_date=time)
    old_sauna = Sauna(pub_date=time)
    self.assertIs(old_house.was_published_recently(), False)
    self.assertIs(old_sauna.was_published_recently(), False)

  def test_was_published_recently_with_recent_structure(self):
    """
    was_published_recently() returns True for structures whose pub_date is within the last day.
    """
    time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
    recent_house = House(pub_date=time)
    recent_sauna = Sauna(pub_date=time)
    self.assertIs(recent_house.was_published_recently(), True)
    self.assertIs(recent_sauna.was_published_recently(), True)
