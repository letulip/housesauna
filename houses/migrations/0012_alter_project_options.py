# Generated by Django 3.2.6 on 2022-02-19 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0011_alter_project_square'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['square']},
        ),
    ]