# Generated by Django 4.2.4 on 2023-09-27 04:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0008_alter_productregister_pcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productregister',
            name='pCategory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Admin.productcategory'),
        ),
    ]
