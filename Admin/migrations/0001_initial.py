# Generated by Django 4.2.4 on 2023-09-25 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Productcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cName', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Productregister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pName', models.CharField(max_length=50, null=True)),
                ('pImage', models.ImageField(max_length=50, null=True, upload_to='')),
                ('pPrice', models.CharField(max_length=50, null=True)),
                ('pQuantity', models.IntegerField(null=True)),
            ],
        ),
    ]