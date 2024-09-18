# Generated by Django 5.1.1 on 2024-09-18 10:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agreements', '0002_agreements_agreement_hash'),
        ('transactions', '0012_alter_transactions_agreement_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='agreement',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='agreements.agreements'),
        ),
    ]
