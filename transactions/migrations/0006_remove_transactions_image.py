# Generated by Django 5.1.1 on 2024-09-08 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_transactions_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactions',
            name='image',
        ),
    ]