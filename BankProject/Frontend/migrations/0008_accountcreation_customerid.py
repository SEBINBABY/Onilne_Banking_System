# Generated by Django 5.0.1 on 2024-01-17 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Frontend', '0007_rename_name_accountcreation_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountcreation',
            name='CUSTOMERID',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]