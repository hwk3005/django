# Generated by Django 5.2.1 on 2025-07-09 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('book_id', models.AutoField(primary_key=True, serialize=False)),
                ('cover', models.URLField(max_length=1500)),
                ('book_url', models.URLField(max_length=1500)),
                ('title', models.CharField(max_length=1000)),
                ('author', models.CharField(max_length=1000)),
                ('publisher', models.CharField(max_length=500)),
                ('pub_date', models.CharField(max_length=500)),
                ('ISBN', models.CharField(max_length=500)),
                ('page', models.IntegerField(default=0)),
                ('size', models.CharField(blank=True, max_length=500)),
                ('review_count', models.IntegerField(default=0)),
                ('bookmark_count', models.IntegerField(default=0)),
                ('rating', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
            ],
        ),
    ]
