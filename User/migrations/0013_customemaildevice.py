# Generated by Django 4.2.4 on 2023-10-04 21:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('User', '0012_wishlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomEmailDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmed', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=64)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='otp_devices', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]