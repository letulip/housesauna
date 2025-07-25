# Generated by Django 5.1.7 on 2025-05-08 13:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("houses", "0017_rename_description_category_description_house_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="header_house",
            field=models.TextField(
                blank=True, null=True, verbose_name="Header (sauna)"
            ),
        ),
        migrations.AddField(
            model_name="category",
            name="header_sauna",
            field=models.TextField(
                blank=True, null=True, verbose_name="Header (sauna)"
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="description_house",
            field=models.TextField(
                blank=True, null=True, verbose_name="Description (house)"
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="description_sauna",
            field=models.TextField(
                blank=True, null=True, verbose_name="Description (sauna)"
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="title_house",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Title (house)"
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="title_sauna",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Title (sauna)"
            ),
        ),
    ]
