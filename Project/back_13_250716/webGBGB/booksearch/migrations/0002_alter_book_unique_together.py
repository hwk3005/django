# Generated by Django 5.2.1 on 2025-07-10 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booksearch', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='book',
            unique_together={('ISBN', 'title', 'author')},
        ),
    ]
