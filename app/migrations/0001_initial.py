# Generated by Django 5.0.4 on 2024-05-03 05:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator])),
                ('password', models.CharField(max_length=250, validators=[django.core.validators.MaxLengthValidator(limit_value=250), django.core.validators.MinLengthValidator(limit_value=8, message='Password must be at least 8 characters')])),
            ],
        ),
    ]
