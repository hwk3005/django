# Generated by Django 5.2.2 on 2025-06-19 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('member_id', models.IntegerField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('id', models.CharField(max_length=50)),
                ('pw', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=50)),
                ('gender', models.CharField(blank=True, max_length=20, null=True)),
                ('birth', models.CharField(blank=True, max_length=100, null=True)),
                ('genres', models.CharField(blank=True, max_length=100, null=True)),
                ('mdate', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
