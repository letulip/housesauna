# Generated by Django 3.2.6 on 2022-02-18 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0008_project_pub_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['square']},
        ),
    ]
