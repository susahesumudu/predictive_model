# Generated by Django 5.1.1 on 2024-09-16 10:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_remove_course_total_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='course',
        ),
        migrations.AddField(
            model_name='schedule',
            name='batch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='course.batch'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='schedule',
            name='module_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.module'),
        ),
    ]
