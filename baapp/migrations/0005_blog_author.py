# Generated by Django 4.2.4 on 2023-08-13 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baapp', '0004_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='author',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
