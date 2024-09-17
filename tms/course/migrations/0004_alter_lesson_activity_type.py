# Generated by Django 5.1.1 on 2024-09-17 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_remove_session_activity_type_lesson_activity_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='activity_type',
            field=models.CharField(choices=[('Lab Exercise', 'Lab Exercise'), ('Assignment', 'Assignment'), ('Assessment', 'Assessment'), ('Project', 'Project'), ('MCQ', 'Multiple-Choice Questions (MCQs)'), ('Presentation', 'Presentation'), ('Workshop', 'Workshop'), ('Practical Lab', 'Practical Lab'), ('Quiz', 'Quiz'), ('Case Study', 'Case Study'), ('Lecture', 'Lecture')], default='Lab Exercise', max_length=50),
        ),
    ]
