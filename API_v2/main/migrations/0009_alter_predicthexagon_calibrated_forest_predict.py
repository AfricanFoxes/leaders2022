# Generated by Django 4.1.3 on 2022-11-05 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_predicthexagon_geometry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predicthexagon',
            name='calibrated_forest_predict',
            field=models.FloatField(null=True),
        ),
    ]