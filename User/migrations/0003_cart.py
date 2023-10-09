# Generated by Django 4.2.4 on 2023-09-28 01:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0010_productregister_pstatus'),
        ('User', '0002_userregister_udob_userregister_uphonenumber'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('total', models.IntegerField(default=0, null=True)),
                ('status', models.IntegerField(default=0)),
                ('productid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Admin.productregister')),
                ('userid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='User.userregister')),
            ],
        ),
    ]