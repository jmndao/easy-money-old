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
        migrations.AddField(
            model_name='clientmodel',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.shop'),
        ),
        migrations.AlterUniqueTogether(
            name='clientmodel',
            unique_together={('fname', 'lname', 'numero')},
        ),
    ]