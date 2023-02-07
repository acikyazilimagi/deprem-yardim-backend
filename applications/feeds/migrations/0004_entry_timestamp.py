# Generated by Django 4.1.6 on 2023-02-07 17:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0003_alter_entry_extra_parameters'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
