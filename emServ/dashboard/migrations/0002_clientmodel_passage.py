# Generated by Django 3.2.3 on 2021-06-17 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientmodel',
            name='passage',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]