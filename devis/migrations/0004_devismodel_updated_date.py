# Generated by Django 3.2.3 on 2021-10-24 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devis', '0003_remove_devismodel_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='devismodel',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]