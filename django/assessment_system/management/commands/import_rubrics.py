from django.core.management.base import BaseCommand
from rubric_assessment.models import Rubric, Criteria

rubrics_data = [
    {
        'name': 'Project Rubric',
        'description': 'A rubric to assess student projects',
        'criteria': [
            {'name': 'Planning and Organization', 'description': 'How well is the project planned?', 'max_points': 20},
            {'name': 'Content Depth', 'description': 'How well is the content understood?', 'max_points': 25},
            {'name': 'Creativity', 'description': 'How creative is the project?', 'max_points': 15},
            {'name': 'Execution', 'description': 'How well was the project executed?', 'max_points': 20},
            {'name': 'Presentation', 'description': 'Quality of presentation', 'max_points': 10},
            {'name': 'Timeliness', 'description': 'Was the project submitted on time?', 'max_points': 5},
        ]
    },
    {
        'name': 'Assignment Rubric',
        'description': 'A rubric for grading assignments',
        'criteria': [
            {'name': 'Knowledge', 'description': 'Demonstrates knowledge of the subject', 'max_points': 25},
            {'name': 'Application', 'description': 'Applies concepts effectively', 'max_points': 20},
            {'name': 'Clarity', 'description': 'Clear and concise communication', 'max_points': 15},
            {'name': 'Analysis', 'description': 'Analytical depth of the work', 'max_points': 20},
            {'name': 'Timeliness', 'description': 'Submitted on time', 'max_points': 5},
        ]
    }
]

class Command(BaseCommand):
    help = 'Imports predefined rubrics and criteria into the database'

    def handle(self, *args, **kwargs):
        for rubric_data in rubrics_data:
            rubric, created = Rubric.objects.get_or_create(
                name=rubric_data['name'], 
                description=rubric_data['description']
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created Rubric: {rubric.name}'))

            for criteria_data in rubric_data['criteria']:
                criteria, criteria_created = Criteria.objects.get_or_create(
                    rubric=rubric,
                    name=criteria_data['name'],
                    description=criteria_data['description'],
                    max_points=criteria_data['max_points']
                )
                if criteria_created:
                    self.stdout.write(self.style.SUCCESS(f'-- Created Criteria: {criteria.name}'))

        self.stdout.write(self.style.SUCCESS('Rubrics and Criteria imported successfully'))

