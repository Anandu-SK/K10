# Generated by Django 4.2.4 on 2023-10-01 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0009_rename_date_order_orderdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='orderdate',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
