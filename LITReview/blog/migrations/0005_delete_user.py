# Generated by Django 3.2.13 on 2022-06-10 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
