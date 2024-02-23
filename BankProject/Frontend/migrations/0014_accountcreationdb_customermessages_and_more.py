# Generated by Django 5.0.1 on 2024-02-10 05:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Frontend', '0013_accountcreationdb_loansanctiondb_reviewratingdb_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerMessages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=100, null=True)),
                ('message', models.CharField(blank=True, max_length=100, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Frontend.userregistrationdb')),
            ],
        ),
    ]
