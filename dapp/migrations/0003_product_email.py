# Generated by Django 4.0 on 2022-02-05 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dapp', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='email',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
