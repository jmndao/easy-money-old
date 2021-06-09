# Generated by Django 3.2.3 on 2021-06-09 08:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_de_la_boutique', models.CharField(max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('achat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.buyingstockmodel')),
                ('clients', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.clientmodel')),
                ('depot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.depositstockmodel')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('produits', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.productmodel')),
                ('requete_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.clientrequestmodel')),
            ],
        ),
    ]
