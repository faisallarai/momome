# Generated by Django 3.2.16 on 2022-11-09 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('payment', '0012_delete_transaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipient_code', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('bank_code', models.CharField(blank=True, max_length=50, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=50, null=True)),
                ('account_name', models.CharField(blank=True, max_length=50, null=True)),
                ('account_number', models.CharField(blank=True, max_length=50, null=True)),
                ('currency', models.CharField(blank=True, max_length=5, null=True)),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('type', models.CharField(blank=True, max_length=50, null=True)),
                ('active', models.BooleanField(blank=True, default=False, null=True)),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('transfer_code', models.CharField(blank=True, max_length=50, null=True)),
                ('transferred_at', models.DateTimeField(blank=True, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('reason', models.TextField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=15, null=True)),
                ('source', models.CharField(blank=True, max_length=15, null=True)),
                ('reference', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.CharField(blank=True, max_length=15, null=True)),
                ('fee_charged', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('recipient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transaction_recipient', to='payment.recipient')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
                'ordering': ('-created_at',),
            },
        ),
    ]