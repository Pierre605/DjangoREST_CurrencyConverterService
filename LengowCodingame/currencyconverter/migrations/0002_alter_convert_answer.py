# Generated by Django 4.1.2 on 2022-10-08 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currencyconverter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convert',
            name='answer',
            field=models.CharField(max_length=50, null=True),
        ),
    ]