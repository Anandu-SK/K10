# Generated by Django 4.2.4 on 2023-09-28 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0009_alter_productregister_pcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='productregister',
            name='pStatus',
            field=models.IntegerField(default=0),
        ),
    ]