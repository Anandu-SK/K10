# Generated by Django 4.2.4 on 2023-09-27 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0005_alter_productregister_pcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productregister',
            name='pCategory',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
