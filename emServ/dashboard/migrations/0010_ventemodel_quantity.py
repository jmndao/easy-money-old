# Generated by Django 3.2.3 on 2021-06-28 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_remove_ventemodel_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='ventemodel',
            name='quantity',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
