# Generated by Django 3.2.16 on 2022-11-05 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_auto_20221104_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='reason',
            field=models.TextField(blank=True, null=True),
        ),
    ]
