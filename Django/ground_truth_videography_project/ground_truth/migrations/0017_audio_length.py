# Generated by Django 2.1.5 on 2023-01-05 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ground_truth', '0016_auto_20221228_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='length',
            field=models.FloatField(default=0),
        ),
    ]
