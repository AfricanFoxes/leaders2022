# Generated by Django 4.1.3 on 2022-11-03 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_pobject_normalize_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='oktmo',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
