# Generated by Django 3.2.3 on 2021-08-02 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_alter_productmodel_matière'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodel',
            name='exact_dimension',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]