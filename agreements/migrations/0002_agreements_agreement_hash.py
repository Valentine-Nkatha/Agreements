# Generated by Django 5.1.1 on 2024-09-18 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agreements', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='agreements',
            name='agreement_hash',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
