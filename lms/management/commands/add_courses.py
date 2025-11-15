from django.core.management.base import BaseCommand
from lms.models import Course


class Command(BaseCommand):
    help = 'Add test courses to the database'

    def handle(self, *args, **kwargs):

        courses = [
            {"name": "First course", "description": "maybe .NET maybe python",
             "created_at": "2025-11-08"},
            {"name": "Second course", "description": "maybe .NET maybe python",
             "created_at": "2025-11-09"},
            {"name": "Third course", "description": "maybe .NET maybe python",
             "created_at": "2025-11-10"}
        ]

        for course_data in courses:
            course, created = Course.objects.get_or_create(**course_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully added course: {course.name}'))
            else:
                self.stdout.write(
                    self.style.WARNING(f'Course already exists: {course.name}'))
