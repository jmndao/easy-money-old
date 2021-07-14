# Generated by Django 3.2.3 on 2021-07-14 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(blank=True, max_length=100, null=True, verbose_name='First Name')),
                ('lname', models.CharField(blank=True, max_length=100, null=True, verbose_name='Last Name')),
                ('nationality', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('age', models.IntegerField()),
                ('numero', models.CharField(blank=True, max_length=20, null=True)),
                ('id_card', models.IntegerField(blank=True, null=True)),
                ('passport_number', models.IntegerField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('passage', models.IntegerField(blank=True, default=0, null=True)),
                ('vente_or_achat', models.CharField(choices=[('CR', 'Client Regulier'), ('CV', 'Vendeur')], default='CR', max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
