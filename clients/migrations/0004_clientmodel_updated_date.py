# Generated by Django 3.2.3 on 2021-10-20 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_clientmodel_invoiced'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientmodel',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]