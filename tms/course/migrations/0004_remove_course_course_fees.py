# Generated by Django 5.1.1 on 2024-09-16 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_remove_course_is_free'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='course_fees',
        ),
    ]
