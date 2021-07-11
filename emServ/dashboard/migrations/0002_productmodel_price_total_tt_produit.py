# Generated by Django 3.2.3 on 2021-07-10 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodel',
            name='price_total_tt_produit',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True, verbose_name="Prix D'Achat Total"),
        ),
    ]
