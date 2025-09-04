import datetime

from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Max
from django.db.models import Q, UniqueConstraint


PRICE_PER_M2_UNDER_70 = 100_000
PRICE_PER_M2_70_TO_150 = 90_000
PRICE_PER_M2_OVER_150 = 80_000

PRICE_PER_M2_CHOICES = [
    (PRICE_PER_M2_UNDER_70, "100 000 ₽/м² (до 70 м²)"),
    (PRICE_PER_M2_70_TO_150, "90 000 ₽/м² (70–150 м²)"),
    (PRICE_PER_M2_OVER_150, "80 000 ₽/м² (свыше 150 м²)"),
]


def _upload_to_structure(instance, filename: str) -> str:
    """
    Формирует путь: <short_name>/<short_name>-<order>.jpeg
    Расширение всегда .jpeg, чтобы URL был стабильным.
    """
    struct = instance.structure
    slug = getattr(struct, 'short_name', None) or getattr(struct, 'slug', None)
    if not slug:
        raise ValidationError('У объекта нет short_name/slug для формирования пути.')
    order = instance.order if instance.order is not None else 0
    return f'{slug}/{slug}-{order}.jpeg'


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
    cost = models.IntegerField('Стоимость', null=True, blank=True)
    video_url = models.CharField('Youtube URL видео', max_length=20)
    description1 = models.TextField('Описание 1', null=True, blank=True)
    description2 = models.TextField('Описание 2', null=True, blank=True)
    complex = models.TextField('Комплектация', null=True, blank=True)
    construction = models.CharField('Время изготовления', max_length=20)
    brus = models.CharField('Характеристика бруса', max_length=20)
    images_count = models.IntegerField('Количество изображений, не заполнять', null=True, blank=True)
    pub_date = models.DateTimeField('Дата публикации')
    price_per_m2 = models.IntegerField(
        choices=PRICE_PER_M2_CHOICES,
        default=PRICE_PER_M2_UNDER_70,
        verbose_name="Цена за м²"
    )

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

    @property
    def cover_image(self):
        return self.images.filter(is_cover=True).first() or self.images.order_by('order').first()


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

    @property
    def cover_image(self):
        return self.images.filter(is_cover=True).first() or self.images.order_by('order').first()


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


class AbstractStructureImage(models.Model):
    """Абстрактный класс для изображений строений."""
    image = models.ImageField(
        'Изображение',
        upload_to=_upload_to_structure
    )
    alt = models.CharField(
        'alt-текст',
        max_length=255,
        blank=True
    )
    order = models.PositiveIntegerField(
        'Порядок отображения',
        default=0,
        db_index=True
    )
    is_cover = models.BooleanField('Обложка', default=False)

    class Meta:
        abstract = True
        ordering = ['-is_cover', 'order', 'id']

    def __str__(self):
        """Отображение имени фото в админке."""
        struct = getattr(self, 'structure', None)
        struct_name = str(struct) if struct else '—'
        role = 'обложка' if self.is_cover else f'#{self.order if self.order is not None else "—"}'
        name = (self.alt or (self.image.name.split('/')[-1] if self.image else 'без файла'))
        return f'{struct_name} · {role} · {name}'

    def clean(self):
        if self.image and hasattr(self.image, 'file'):
            try:
                from PIL import Image
                self.image.file.seek(0)
                img = Image.open(self.image.file)
                if img.format not in ('JPEG', 'JPG'):
                    raise ValidationError('Только JPEG изображения допускаются.')
            except Exception:
                raise ValidationError('Невалидное изображение. Загрузите JPEG.')

    def _next_order(self) -> int:
        """
        Найти следующий order для конкретного объекта (House/Sauna).
        """
        qs = self.__class__.objects.filter(structure=self.structure)
        m = qs.aggregate(m=Max('order'))['m']
        return 0 if m is None else (m + 1)

    def save(self, *args, **kwargs):
        if self.order is None:
            self.order = self._next_order()
        super().save(*args, **kwargs)
        if self.is_cover:
            self.__class__.objects.filter(structure=self.structure) \
                .exclude(pk=self.pk).update(is_cover=False)


class HouseImage(AbstractStructureImage):
    """Изображения домов."""
    structure = models.ForeignKey(
        'House',
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Дом',
    )

    class Meta:
        verbose_name = 'Фото дома'
        verbose_name_plural = 'Фото дома'
        constraints = [
            UniqueConstraint(
                fields=['structure'],
                condition=Q(is_cover=True),
                name='unique_house_cover_per_structure',
            ),
            UniqueConstraint(
                fields=['structure', 'order'],
                name='unique_house_structure_order'),
        ]


class SaunaImage(AbstractStructureImage):
    """Изображения бань."""
    structure = models.ForeignKey(
        'Sauna',
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Баня',
    )

    class Meta:
        verbose_name = 'Фото бани'
        verbose_name_plural = 'Фото бани'
        constraints = [
            UniqueConstraint(
                fields=['structure'],
                condition=Q(is_cover=True),
                name='unique_sauna_cover_per_structure',
            ),
            UniqueConstraint(
                fields=['structure', 'order'],
                name='unique_sauna_structure_order'),
        ]
