# Generated by Django 2.2 on 2019-04-17 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20190416_1749'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='thumb',
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='media'),
        ),
    ]
