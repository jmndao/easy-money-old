# Generated by Django 3.2.3 on 2021-06-14 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_alter_productmodel_annee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmodel',
            name='poids',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True, verbose_name='Masse'),
        ),
    ]