import datetime

from django.utils import timezone
from django.db import models


PRICE_PER_M2_UNDER_70 = 100_000
PRICE_PER_M2_70_TO_150 = 90_000
PRICE_PER_M2_OVER_150 = 80_000


class AbstractHouse(models.Model):
    """
    Базовая модель для домов и бань.
    """
    full_name = models.CharField('URL название', max_length=200, unique=True)
    slug = models.SlugField('Короткий тег', max_length=300, unique=True)
    short_name = models.CharField('URL сокращ. название', max_length=200, unique=True)
    title = models.CharField('Заголовок', max_length=200)
    dimensions = models.CharField('Габариты', max_length=15)
    square = models.FloatField('Общая площадь (м²)')
    square1 = models.CharField('Доп. площадь 1', max_length=15, null=True, blank=True)
    square2 = models.CharField('Доп. площадь 2', max_length=15, null=True, blank=True)
    cost = models.IntegerField('Стоимость')
    video_url = models.CharField('Youtube URL видео', max_length=20)
    cover = models.CharField('Обложка', max_length=30, null=True, blank=True)
    description1 = models.TextField('Описание 1', null=True, blank=True)
    description2 = models.TextField('Описание 2', null=True, blank=True)
    complex = models.TextField('Комплектация', null=True, blank=True)
    construction = models.CharField('Тип конструкции', max_length=20)
    brus = models.CharField('Характеристика бруса', max_length=20)
    images_count = models.IntegerField('Количество изображений')
    pub_date = models.DateTimeField('Дата публикации')
    price_per_m2 = models.IntegerField(default=0, verbose_name='Цена за м²')

    class Meta:
        abstract = True

    def was_published_recently(self) -> bool:
        """
        True, если опубликовано за последние 24 часа.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def update_cost(self):
        """
        Метод для обновления основной цены при изменении стоимости за кв.м.
        Вызываем в shell в цикле вручную по всем домам один раз
        после изменения цены за кв.м.

        python manage.py shell
        from houses.models import Sauna/House
        for house in Sauna/House.objects.all():
            house.assign_initial_price_per_m2()
            house.update_cost()
        """
        if self.square and self.price_per_m2:
            self.cost = self.square * self.price_per_m2
            self.save(update_fields=["cost"])

    def assign_initial_price_per_m2(self):
        """
        Однократная логика назначения цены за м² в БД на основе площади.
        Логика распределения цены предоставлена заказчиком.
        """
        if self.square < 70:
            self.price_per_m2 = PRICE_PER_M2_UNDER_70
        elif self.square <= 150:
            self.price_per_m2 = PRICE_PER_M2_70_TO_150
        else:
            self.price_per_m2 = PRICE_PER_M2_OVER_150
        self.save(update_fields=["price_per_m2"])

    def __str__(self) -> str:
        return self.full_name


class Category(models.Model):
    """
    Категория для домов, бань и проектов.
    """
    name = models.CharField('Category\'s name', max_length=60, unique=True)
    slug = models.SlugField('Category\'s slug', blank=True, null=True)
    priority = models.SmallIntegerField('Priority', default=1)
    subcategory = models.ManyToManyField(
        'Category',
        verbose_name='Subcategory',
        blank=True,
        related_name='parent'
    )
    # SEO поля
    title_house = models.CharField(
        'Title (house)', max_length=255, null=True, blank=True)
    description_house = models.TextField(
        'Description (house)', null=True, blank=True)
    title_sauna = models.CharField(
        'Title (sauna)', max_length=255, null=True, blank=True)
    description_sauna = models.TextField(
        'Description (sauna)', null=True, blank=True)
    header_sauna = models.TextField(
        'Header (sauna)', null=True, blank=True)
    header_house = models.TextField(
        'Header (house)', null=True, blank=True)
    subcategories_description = models.JSONField(
        'Subcategories description', null=True, blank=True)

    class Meta:
        ordering = ('priority', 'name')
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class House(AbstractHouse):
    """
    Построенный дом.
    """
    dir_name = 'Построенные дома'
    class_name = 'House'
    category = models.ManyToManyField(
        Category,
        verbose_name='category',
        blank=True,
        related_name='houses'
    )

    '''
    House object example:
    full_name='house-122-meters',
    short_name='house-122',
    title='Дом из клееного бруса для постоянного проживания',
    dimensions='9,2x8,6',
    square='122',
    square1='71,7',
    square2='50,6',
    cost='6 000 000',
    video_url='bU_CYEp0y5M',
    cover='',
    description1='',
    description2='',
    complex='',
    construction='ДВА месяца',
    brus='Ш 174/ В 140',
    images_count=7,
    pub_date=timezone.now()
    '''

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Дом'
        verbose_name_plural = 'Дома'


class Sauna(AbstractHouse):
    """
    Построенная баня.
    """
    dir_name = 'Построенные дома-бани'
    class_name = 'Sauna'
    category = models.ManyToManyField(
        Category,
        verbose_name='category',
        blank=True,
        related_name='saunas'
    )

    '''
    Sauna object example:
    full_name='house-sauna-130-meters',
    short_name='house-sauna-130',
    title='Дом Баня из клееного бруса',
    dimensions='9,0x12,0',
    square='130',
    square1='',
    square2='',
    cost='7 150 000',
    video_url='YW8b3dcT6_A',
    cover='',
    description1='',
    description2='',
    complex='',
    construction='ДВА месяца',
    brus='Ш 130/ В 140',
    images_count=20,
    pub_date=timezone.now()
    '''

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Баня'
        verbose_name_plural = 'Бани'


class Project(models.Model):
    """
    Модель проектных домов и бань (ещё не построенных, только чертежи).

    Используется для показа клиентам будущих решений, которые можно заказать:
    - Хранит превью изображения, площадь, размеры и категории.
    - Площадь хранится как float, чтобы использовать фильтрацию по диапазону.

    Поля:
    - full_name: Уникальное название проекта.
    - slug: Человекочитаемый URL.
    - short_name: Сокращённое имя (например, для папок с изображениями).
    - title: Заголовок карточки проекта.
    - dimensions: Размеры.
    - square: Площадь (в м²).
    - image: Изображение-превью.
    - pub_date: Дата публикации.
    - category: Категории проекта.
    """

    full_name = models.CharField('URL название', max_length=200)
    slug = models.SlugField('Короткий тег', max_length=300, unique=True)
    short_name = models.CharField('URL сокращ. название',max_length=200)
    title = models.CharField('Заголовок', max_length=200)
    dimensions = models.CharField('Габариты', max_length=15)
    square = models.FloatField('Общая площадь (м²)')
    image = models.ImageField(
        'Превью проекта',
        upload_to='projects/',
    )
    pub_date = models.DateTimeField('date published')
    category = models.ManyToManyField(
        Category,
        verbose_name='Категории',
        blank=True,
        related_name='projects'
    )

    def __str__(self):
        return self.full_name

    class Meta():
        ordering = ['square']
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
