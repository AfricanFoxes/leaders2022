# Generated by Django 4.1.3 on 2022-11-03 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_region_prc_employees_small_businesses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pobject',
            name='normalize_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='region',
            name='normalize_name',
            field=models.CharField(max_length=100),
        ),
    ]
