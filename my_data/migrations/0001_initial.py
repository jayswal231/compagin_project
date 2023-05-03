# Generated by Django 3.2.12 on 2023-05-02 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=500, null=True)),
                ('name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Participants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('affiliated_org', models.CharField(blank=True, max_length=500)),
                ('designation', models.CharField(blank=True, max_length=500)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female'), ('others', 'others')], default='male', max_length=500)),
                ('ethinicity', models.CharField(blank=True, choices=[('dalit', 'dalit')], max_length=500)),
                ('pwd', models.BooleanField(blank=True, null=True)),
                ('participation_category', models.CharField(blank=True, max_length=1000)),
                ('contact', models.IntegerField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('step1_user', models.CharField(blank=True, max_length=500, null=True)),
                ('step1', models.BooleanField(blank=True, null=True)),
                ('step2_user', models.CharField(blank=True, max_length=500, null=True)),
                ('step2', models.BooleanField(blank=True, null=True)),
                ('step3_user', models.CharField(blank=True, max_length=500, null=True)),
                ('step3', models.BooleanField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=500, null=True)),
                ('name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('province', models.CharField(max_length=500)),
                ('district', models.CharField(max_length=500)),
                ('palika', models.CharField(blank=True, max_length=500)),
                ('ward', models.IntegerField(blank=True, null=True)),
                ('community', models.CharField(blank=True, max_length=500)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('person_responsible', models.CharField(blank=True, max_length=100)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_data.activity')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_data.project')),
            ],
        ),
        migrations.AddField(
            model_name='activity',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_data.project'),
        ),
        migrations.CreateModel(
            name='Actions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actions', models.CharField(choices=[('list', 'list'), ('create', 'create'), ('update', 'update'), ('delete', 'delete')], default='list', max_length=50)),
                ('current_state', models.JSONField(blank=True, null=True)),
                ('user', models.CharField(blank=True, max_length=1000, null=True)),
                ('group', models.CharField(blank=True, max_length=1000, null=True)),
                ('participants', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='my_data.participants')),
            ],
        ),
    ]
