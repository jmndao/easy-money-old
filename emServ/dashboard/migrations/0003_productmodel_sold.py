# Generated by Django 3.2.3 on 2021-06-18 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_clientmodel_passage'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodel',
            name='sold',
            field=models.BooleanField(default=False),
        ),
    ]