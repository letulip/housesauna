# Generated by Django 3.2.6 on 2022-02-19 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0010_alter_project_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='square',
            field=models.IntegerField(max_length=15),
        ),
    ]
