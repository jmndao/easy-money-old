# Generated by Django 3.2.3 on 2021-06-30 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_auto_20210630_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmodel',
            name='obsolescence',
            field=models.CharField(blank=True, choices=[('TRES_RAPIDE', 'Tres_Rapide'), ('RAPIDE', 'Rapide'), ('MOYENNE', 'Moyenne'), ('LENTE', 'Lente')], max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='EstimationModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='First Name')),
                ('product_name', models.CharField(max_length=100)),
                ('new_price', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True, verbose_name='Prix neuf')),
                ('used_price', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True, verbose_name='Prix occasion')),
                ('estate', models.CharField(blank=True, choices=[('NEUF', 'Neuf'), ('BON', 'Bon'), ('MOYEN', 'Moyen'), ('MAUVAIS', 'Mauvais'), ('POUR_PIECE', 'Pour Piece')], max_length=20, null=True)),
                ('obsolescence', models.CharField(blank=True, choices=[('TRES_RAPIDE', 'Tres_Rapide'), ('RAPIDE', 'Rapide'), ('MOYENNE', 'Moyenne'), ('LENTE', 'Lente')], max_length=20, null=True)),
                ('rarety', models.CharField(blank=True, choices=[('RARE', 'Rare'), ('COURANT', 'Courant'), ('TRES_COURANT', 'Tres courant')], max_length=20, null=True)),
                ('sale_bill', models.BooleanField(default=False)),
                ('dimension', models.CharField(blank=True, choices=[('PETIT', 'Petit'), ('MOYEN', 'Moyen'), ('GRAND', 'Grand')], max_length=20, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('charger', models.BooleanField(default=False)),
                ('original_box', models.BooleanField(default=False)),
                ('year_of_release', models.IntegerField(blank=True, null=True)),
                ('shop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.shop')),
            ],
        ),
    ]
