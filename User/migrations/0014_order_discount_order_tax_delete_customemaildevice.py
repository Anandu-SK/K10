# Generated by Django 4.2.4 on 2023-10-06 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0013_customemaildevice'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='tax',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.DeleteModel(
            name='CustomEmailDevice',
        ),
    ]
