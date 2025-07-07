import pytest
from django.utils import timezone
from datetime import timedelta
from houses.models import House, Sauna, Project, Category


@pytest.mark.django_db
class TestAbstractHouseModels:
    def create_house(self, **kwargs):
        """
        Создание объекта House с дефолтными значениями.
        """
        return House.objects.create(
            full_name=kwargs.get("full_name", "Test House"),
            slug=kwargs.get("slug", "test-house"),
            short_name=kwargs.get("short_name", "house"),
            title=kwargs.get("title", "Тестовый дом"),
            dimensions=kwargs.get("dimensions", "10x10"),
            square=kwargs.get("square", "100"),
            square1=kwargs.get("square1", "50"),
            square2=kwargs.get("square2", "50"),
            cost=kwargs.get("cost", "5 000 000"),
            video_url=kwargs.get("video_url", "abc123"),
            cover=kwargs.get("cover", ""),
            description1=kwargs.get("description1", ""),
            description2=kwargs.get("description2", ""),
            complex=kwargs.get("complex", ""),
            construction=kwargs.get("construction", "2 месяца"),
            brus=kwargs.get("brus", "Ш 150/ В 140"),
            images_count=7,
            pub_date=kwargs.get("pub_date", timezone.now())
        )

    def test_str_representation(self):
        """Метод __str__ возвращает полное название дома."""
        house = self.create_house(full_name="Дом №1")
        assert str(house) == "Дом №1"

    def test_was_published_recently_true(self):
        """was_published_recently возвращает True, если дата в пределах 24 часов."""
        recent_house = self.create_house(pub_date=timezone.now() - timedelta(hours=12))
        assert recent_house.was_published_recently() is True

    def test_was_published_recently_false(self):
        """was_published_recently возвращает False, если дата старше 24 часов."""
        old_house = self.create_house(pub_date=timezone.now() - timedelta(days=2))
        assert old_house.was_published_recently() is False

    def test_ordering_by_pub_date(self):
        """Объекты сортируются по убыванию pub_date (самый новый — первым)."""
        old = self.create_house(full_name="Старый", slug="old", short_name="old", pub_date=timezone.now() - timedelta(days=10))
        new = self.create_house(full_name="Новый", slug="new", short_name="new", pub_date=timezone.now())
        houses = list(House.objects.all())
        assert houses[0] == new
        assert houses[1] == old


@pytest.mark.django_db
class TestCategoryModel:

    def test_str_representation(self):
        """Метод __str__ возвращает имя категории."""
        category = Category.objects.create(name="Малые дома", slug="small")
        assert str(category) == "Малые дома"

    def test_category_subcategory_relationship(self):
        """Категория может содержать подкатегории через M2M."""
        parent = Category.objects.create(name="Дома", slug="home")
        child = Category.objects.create(name="Бани", slug="sauna")
        parent.subcategory.add(child)
        assert child in parent.subcategory.all()


@pytest.mark.django_db
class TestSaunaModel:

    def test_sauna_creation(self):
        """Создаем объект Sauna с дефолтными значениями."""
        sauna = Sauna.objects.create(
            full_name="Сауна №1",
            slug="sauna-1",
            short_name="sauna",
            title="Красивая баня",
            dimensions="8x8",
            square="64",
            cost="3 000 000",
            video_url="def456",
            construction="1 месяц",
            brus="Ш 130/ В 140",
            images_count=5,
            pub_date=timezone.now()
        )
        assert isinstance(sauna, Sauna)
        assert sauna.full_name == "Сауна №1"


@pytest.mark.django_db
class TestProjectModel:

    def test_project_creation_and_str(self):
        """Создаем проект и получаем его название через __str__."""
        category = Category.objects.create(name="Проекты", slug="projects")
        project = Project.objects.create(
            full_name="Проект A",
            slug="project-a",
            short_name="projA",
            title="Дом A",
            dimensions="10x15",
            square=150.5,
            image="projects/fake.jpg",
            pub_date=timezone.now()
        )
        project.category.add(category)
        assert str(project) == "Проект A"
        assert category in project.category.all()

    def test_project_ordering_by_square(self):
        """Проекты сортируются по возрастанию площади square."""
        Project.objects.create(
            full_name="P1", slug="p1", short_name="p1", title="p1",
            dimensions="8x8", square=64.0,
            image="projects/p1.jpg", pub_date=timezone.now()
        )
        Project.objects.create(
            full_name="P2", slug="p2", short_name="p2", title="p2",
            dimensions="10x10", square=100.0,
            image="projects/p2.jpg", pub_date=timezone.now()
        )
        projects = list(Project.objects.all())
        assert projects[0].square < projects[1].square
