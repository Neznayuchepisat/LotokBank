# Generated by Django 5.1.1 on 2024-11-17 16:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banklotkov', '0003_balancerequest_loan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balancerequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banklotkov.profile'),
        ),
    ]
