# Generated by Django 5.0.4 on 2024-05-03 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='images')),
            ],
        ),
        migrations.AddField(
            model_name='usermodel',
            name='images',
            field=models.ImageField(default='', upload_to='', verbose_name='images'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usermodel',
            name='title',
            field=models.CharField(default=' ', max_length=50),
            preserve_default=False,
        ),
    ]
