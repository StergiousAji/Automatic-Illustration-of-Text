# Generated by Django 2.1.5 on 2023-01-05 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ground_truth', '0017_audio_length'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audio',
            name='length',
        ),
    ]
