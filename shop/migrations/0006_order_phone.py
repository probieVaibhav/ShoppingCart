# Generated by Django 3.0.6 on 2020-06-03 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20200603_1240'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(default='', max_length=12),
        ),
    ]
