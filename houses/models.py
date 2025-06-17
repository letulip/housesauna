import datetime
from django.utils import timezone
from django.db import models


class AbstractHouse(models.Model):
    """
    Абстрактная модель для общего описания домов и бань.

    Содержит основные поля, общие для моделей House и Sauna:
    - full_name: Уникальное полное имя объекта, используется как ID.
    - slug: Уникальный человекочитаемый идентификатор для URL.
    - short_name: Сокращённое имя, часто используется для путей к изображениям.
    - title: Название проекта/объекта.
    - dimensions: Габариты строения (например, "9,2x8,6").
    - square: Общая площадь.
    - square1/square2: Дополнительные площади этажей (если есть).
    - cost: Стоимость объекта.
    - video_url: Идентификатор видео на YouTube.
    - cover: Название обложки (опционально).
    - description1/description2: Текстовые описания для карточки или страницы.
    - complex: Комплектация дома/бани (опционально).
    - construction: Срок строительства.
    - brus: Размеры бруса.
    - images_count: Кол-во изображений в галерее.
    - pub_date: Дата публикации.
    """

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

    class Meta:
        abstract = True


class Category(models.Model):
    """
    Категория или подкатегория объектов (домов, бань, проектов).

    Используется для организации структуры каталога:
    - Может иметь подкатегории (ManyToMany к себе).
    - Имеет отдельные поля описания и заголовков для домов и бань.

    Поля:
    - name: Название категории.
    - slug: Уникальный идентификатор для URL.
    - priority: Приоритет сортировки (меньше — выше).
    - subcategory: Подкатегории (дерево).
    - title_house / description_house: SEO-данные для домов.
    - title_sauna / description_sauna: SEO-данные для бань.
    - header_house / header_sauna: Текстовые заголовки в списках.
    - subcategories_description: JSON с описаниями вложенных категорий.
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
    title_house = models.CharField('Title (house)', max_length=255, null=True, blank=True)
    description_house = models.TextField('Description (house)', null=True, blank=True)
    title_sauna = models.CharField('Title (sauna)', max_length=255, null=True, blank=True)
    description_sauna = models.TextField('Description (sauna)', null=True, blank=True)
    header_sauna = models.TextField('Header (sauna)', null=True, blank=True)
    header_house = models.TextField('Header (house)', null=True, blank=True)
    subcategories_description = models.JSONField('Subcategories description', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('priority', 'name')

    def __str__(self):
        return self.name


class House(AbstractHouse):
    """
    Модель построенного дома из клееного бруса.

    Наследует поля из AbstractHouse. Хранит категории, к которым относится дом.
    Используется в ленте последних проектов,
    списках домов и детальных карточках.

    Поля:
    - category: Категории дома (одноэтажные, с террасой и т.п.)
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

    def __str__(self):
        return self.full_name

    def was_published_recently(self):
        """
        Возвращает True, если объект опубликован за последние 24 часа.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    class Meta:
        ordering = ['-pub_date']


class Sauna(AbstractHouse):
    """
    Модель построенной бани (или дома-баня) из клееного бруса.

    Наследует поля из AbstractHouse.
    Хранит категории, к которым относится баня.
    Используется аналогично House в списках и карточках.

    Поля:
    - category: Категории бани (например, «с мансардой», «на 2 этажа»).
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

    def __str__(self):
        return self.full_name

    def was_published_recently(self) -> bool:
        """
        Возвращает True, если объект опубликован за последние 24 часа.
        """

        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    class Meta:
        ordering = ['-pub_date']


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

    full_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=300, unique=True)
    short_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    dimensions = models.CharField(max_length=15)
    square = models.FloatField(max_length=15)
    image = models.ImageField(
        'Превью проекта',
        upload_to='projects/',
    )
    pub_date = models.DateTimeField('date published')
    category = models.ManyToManyField(
        Category,
        verbose_name='category',
        blank=True,
        related_name='projects'
    )

    def __str__(self):
        return self.full_name

    class Meta():
        ordering = ['square']
