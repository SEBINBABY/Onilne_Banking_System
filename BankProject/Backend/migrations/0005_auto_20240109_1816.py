# Generated by Django 3.1.8 on 2024-01-09 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0004_auto_20240109_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountdb',
            name='ACCFULLDESC',
            field=models.CharField(blank=True, max_length=2500, null=True),
        ),
    ]