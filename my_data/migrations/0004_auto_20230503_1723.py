# Generated by Django 3.2.7 on 2023-05-03 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_data', '0003_auto_20230503_1206'),
    ]

    operations = [
        migrations.RenameField(
            model_name='participants',
            old_name='ethinicity',
            new_name='ethnicity',
        ),
        migrations.AddField(
            model_name='participants',
            name='person_responsible',
            field=models.CharField(blank=True, max_length=99, null=True),
        ),
    ]
