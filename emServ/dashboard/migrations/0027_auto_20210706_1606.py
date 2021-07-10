# Generated by Django 3.2.3 on 2021-07-06 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0026_auto_20210706_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientmodel',
            name='id_card',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='clientmodel',
            name='passport_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='price_vente_minimum_ad',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=20, null=True, verbose_name='Prix Vente Minimu'),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='price_vente_minimum_dv',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=20, null=True, verbose_name='Prix Vente Minimu'),
        ),
    ]
