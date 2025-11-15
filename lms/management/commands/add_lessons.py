from django.core.management.base import BaseCommand
from lms.models import Lesson, Course


class Command(BaseCommand):
    help = 'Add test courses to the database'

    def handle(self, *args, **kwargs):
        course1, _ = Course.objects.get_or_create(id=1)
        course2, _ = Course.objects.get_or_create(id=2)
        course3, _ = Course.objects.get_or_create(id=3)

        lessons = [
            {"name": "First lesson by first course", "description": "maybe .NET maybe python",
             "created_at": "2025-11-08", "course": course1},
            {"name": "Second lesson by first course", "description": "maybe .NET maybe python",
             "created_at": "2025-11-08", "course": course1},
            {"name": "Third lesson by first course", "description": "maybe .NET maybe python",
             "created_at": "2025-11-08", "course": course1},
            {"name": "First lesson by Second course", "description": "maybe .NET maybe python",
             "created_at": "2025-11-09", "course": course2},
            {"name": "Second lesson by Second course", "description": "maybe .NET maybe python",
             "created_at": "2025-11-09", "course": course2},
            {"name": "Third lesson by Second course", "description": "maybe .NET maybe python",
             "created_at": "2025-11-09", "course": course2},
            {"name": "First lesson by Third course", "description": "maybe .NET maybe python",
             "created_at": "2025-11-10", "course": course3},
            {"name": "Second lesson by Third course", "description": "maybe .NET maybe python",
             "created_at": "2025-11-10", "course": course3},
            {"name": "Third lesson by Third course", "description": "maybe .NET maybe python",
             "created_at": "2025-11-10", "course": course3}
        ]

        for lesson_data in lessons:
            lesson, created = Lesson.objects.get_or_create(**lesson_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully added lesson: {lesson.name}'))
            else:
                self.stdout.write(
                    self.style.WARNING(f'Lesson already exists: {lesson.name}'))
