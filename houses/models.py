import datetime
from django.utils import timezone
from django.db import models


# Create your models here.
class House(models.Model):
    dir_name = 'Построенные дома'
    class_name = 'House'
    full_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=300, unique=True)
    short_name = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=200)
    dimensions = models.CharField(max_length=15)
    square = models.CharField(max_length=15)
    square1 = models.CharField(max_length=15, null=True, blank=True)
    square2 = models.CharField(max_length=15, null=True, blank=True)
    cost = models.CharField(max_length=15)
    video_url = models.CharField(max_length=20)
    cover = models.CharField(max_length=30, null=True, blank=True)
    description1 = models.TextField(null=True, blank=True)
    description2 = models.TextField(null=True, blank=True)
    complex = models.TextField(serialize=True, null=True, blank=True)
    construction = models.CharField(max_length=20)
    brus = models.CharField(max_length=20)
    images_count = models.IntegerField()
    pub_date = models.DateTimeField('date published')

    '''
    House object example:
    full_name='house-122-meters', short_name='house-122', title='Дом из клееного бруса для постоянного проживания', dimensions='9,2x8,6', square='122', square1='71,7', square2='50,6', cost='6 000 000', video_url='bU_CYEp0y5M', cover='', description1='', description2='', complex='', construction='ДВА месяца', brus='Ш 174/ В 140', images_count=7, pub_date=timezone.now()
    ''' 

    def __str__(self) -> str:
        return self.full_name

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    class Meta():
        ordering = ['-pub_date']


class Sauna(models.Model):
    dir_name = 'Построенные дома-бани'
    class_name = 'Sauna'
    full_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=300, unique=True)
    short_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    dimensions = models.CharField(max_length=15)
    square = models.CharField(max_length=15)
    square1 = models.CharField(max_length=15, null=True, blank=True)
    square2 = models.CharField(max_length=15, null=True, blank=True)
    cost = models.CharField(max_length=15)
    video_url = models.CharField(max_length=20)
    cover = models.CharField(max_length=30, null=True, blank=True)
    description1 = models.TextField(null=True, blank=True)
    description2 = models.TextField(null=True, blank=True)
    complex = models.TextField(serialize=True, null=True, blank=True)
    construction = models.CharField(max_length=20)
    brus = models.CharField(max_length=20)
    images_count = models.IntegerField()
    pub_date = models.DateTimeField('date published')

    '''
    Sauna object example:
    full_name='house-sauna-130-meters', short_name='house-sauna-130', title='Дом Баня из клееного бруса', dimensions='9,0x12,0', square='130', square1='', square2='', cost='7 150 000', video_url='YW8b3dcT6_A', cover='', description1='', description2='', complex='', construction='ДВА месяца', brus='Ш 130/ В 140', images_count=20, pub_date=timezone.now()
    '''

    def __str__(self) -> str:
        return self.full_name

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    class Meta():
        ordering = ['-pub_date']
