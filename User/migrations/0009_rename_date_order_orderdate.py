# Generated by Django 4.2.4 on 2023-10-01 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0008_order_total_bill'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='date',
            new_name='orderdate',
        ),
    ]
