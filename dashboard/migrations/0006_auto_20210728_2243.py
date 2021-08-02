# Generated by Django 3.2.3 on 2021-07-28 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_alter_productmodel_matière'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productmodel',
            old_name='matière',
            new_name='material',
        ),
        migrations.AddField(
            model_name='productmodel',
            name='delai_garantie',
            field=models.IntegerField(blank=True, default=True, null=True),
        ),
    ]
