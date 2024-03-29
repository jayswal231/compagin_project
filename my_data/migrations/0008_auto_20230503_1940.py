# Generated by Django 3.2.7 on 2023-05-03 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_data', '0007_auto_20230503_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='submit_one',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='submit_three',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='submit_two',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='participants',
            name='ethnicity',
            field=models.CharField(blank=True, choices=[('dalit', 'Dalit')], max_length=500),
        ),
    ]
