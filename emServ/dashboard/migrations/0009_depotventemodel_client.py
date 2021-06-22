# Generated by Django 3.2.3 on 2021-06-22 17:15

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_alter_productmodel_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='depotventemodel',
            name='client',
            field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.clientmodel'),
            preserve_default=False,
        ),
    ]