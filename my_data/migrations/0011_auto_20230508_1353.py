# Generated by Django 3.2.7 on 2023-05-08 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_data', '0010_auto_20230508_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participants',
            name='step1',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='participants',
            name='step2',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='participants',
            name='step3',
            field=models.BooleanField(default=False),
        ),
    ]