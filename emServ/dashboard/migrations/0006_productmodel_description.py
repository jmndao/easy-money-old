# Generated by Django 3.2.3 on 2021-06-26 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_productmodel_montant_restauration'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodel',
            name='description',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
    ]