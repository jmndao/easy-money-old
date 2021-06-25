<<<<<<< HEAD
# Generated by Django 3.2.3 on 2021-06-25 10:18
=======
# Generated by Django 3.2.3 on 2021-06-24 22:23
>>>>>>> a0b1d1d30c0e25b203e1c292f8c59b8378eaf3b0

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0006_alter_userprofile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(blank=True, max_length=100, null=True, verbose_name='First Name')),
                ('lname', models.CharField(blank=True, max_length=100, null=True, verbose_name='Last Name')),
                ('nationality', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('sexe', models.CharField(choices=[('H', 'Homme'), ('F', 'Femme')], max_length=1)),
                ('age', models.IntegerField()),
                ('numero', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('passage', models.IntegerField(default=1)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('model', models.CharField(blank=True, max_length=100, null=True)),
                ('category', models.CharField(blank=True, choices=[('ELECTRONIQUE', 'Electronique'), ('VETEMENT', 'Vetement'), ('DECORATIONS', 'Decorations'), ('ENFANT', 'Telephoniques'), ('AMMEUBLEMENT', 'Ammeublement'), ('LOISIRS', 'Loisirs'), ('IMAGES_ET_SONS', 'Images_et_sons'), ('AUTRES', 'Autre')], max_length=100, null=True)),
                ('dv_or_ad', models.CharField(blank=True, choices=[('DV', 'Depot Vente'), ('AD', 'Achat Direct')], max_length=100, null=True)),
                ('vente_or_achat', models.CharField(choices=[('ACHAT', 'Achat'), ('VENTE', 'Vente')], max_length=100)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True, verbose_name="Prix d'Achat")),
                ('estate', models.CharField(blank=True, choices=[('NEUF', 'Neuf'), ('BON', 'Bon'), ('MOYEN', 'Moyen'), ('MAUVAIS', 'Mauvais'), ('POUR_PIECE', 'Pour Piece')], max_length=20, null=True)),
                ('obsolescence', models.CharField(blank=True, choices=[('RAPIDE', 'Rapide'), ('MOYENNE', 'Moyenne'), ('LENTE', 'Lente')], max_length=20, null=True)),
                ('rarety', models.CharField(blank=True, choices=[('RARE', 'Rare'), ('COURANT', 'Courant'), ('TRES_COURANT', 'Tres courant')], max_length=20, null=True)),
                ('sale_bill', models.BooleanField(default=False)),
                ('dimension', models.CharField(blank=True, choices=[('PETIT', 'Petit'), ('MOYEN', 'Moyen'), ('GRAND', 'Grand')], max_length=20, null=True)),
                ('edition', models.CharField(blank=True, max_length=100, null=True)),
                ('annee', models.CharField(blank=True, max_length=20, null=True)),
                ('storage', models.IntegerField(blank=True, null=True)),
                ('ram', models.IntegerField(blank=True, null=True)),
                ('charger', models.BooleanField(default=True)),
                ('original_box', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('sold', models.BooleanField(default=False)),
                ('color', models.CharField(blank=True, max_length=100, null=True)),
                ('seller', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.clientmodel')),
            ],
        ),
        migrations.CreateModel(
            name='VenteModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True, verbose_name='Prix De Vente Final')),
                ('acompte', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True, verbose_name="l'avance du client")),
                ('guarantee', models.BooleanField(default=False)),
                ('guarantee_period', models.IntegerField(blank=True, null=True, verbose_name='Periode de garantie [en mois]')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.clientmodel')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.productmodel')),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('emplacement', models.CharField(blank=True, max_length=100, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='productmodel',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.shop'),
        ),
        migrations.CreateModel(
            name='DepotVenteModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True, verbose_name='Prix de vente minimum')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.productmodel')),
            ],
        ),
        migrations.CreateModel(
            name='ClientRequestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('produit_demander', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('found', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.clientmodel')),
            ],
        ),
        migrations.AddField(
            model_name='clientmodel',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.shop'),
        ),
        migrations.CreateModel(
            name='AchatDirectModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=3, max_digits=20, verbose_name="Prix d'achat")),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.clientmodel')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.productmodel')),
            ],
        ),
    ]
