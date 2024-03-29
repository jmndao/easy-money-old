# Generated by Django 3.2.3 on 2021-07-14 00:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0001_initial'),
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VenteModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True, verbose_name='Prix De Vente')),
                ('price_total', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True, verbose_name='Prix De Vente Final')),
                ('acompte', models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=20, null=True, verbose_name="L'avance du client")),
                ('restant_du', models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=20, null=True, verbose_name='Restant du Client')),
                ('guarantee', models.BooleanField(default=False)),
                ('guarantee_period', models.IntegerField(blank=True, null=True, verbose_name='Periode de garantie [en mois]')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField(blank=True, default=1, null=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='clients.clientmodel')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.productmodel')),
            ],
        ),
    ]
