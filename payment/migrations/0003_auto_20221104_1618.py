# Generated by Django 3.2.16 on 2022-11-04 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_auto_20221104_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipient',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='reference',
            field=models.UUIDField(blank=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transfer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transaction_transfer', to='payment.transfer'),
        ),
    ]