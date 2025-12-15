from django.core.management.base import BaseCommand
from django.utils import timezone
from schedule.models import Project, Person, Presentation

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Create projects
        sfb1368, _ = Project.objects.get_or_create(name="Project A", defaults={'category': 'RES'})
        trr277, _ = Project.objects.get_or_create(name="Project B", defaults={'category': 'RES'})
        siemens_asg, _ = Project.objects.get_or_create(name="Project C", defaults={'category': 'IND'})

        # Create people
        sandra, _ = Person.objects.get_or_create(first_name="Alex", last_name="Doe", defaults={'is_active': True})
        sebastian, _ = Person.objects.get_or_create(first_name="Jordan", last_name="Smith", defaults={'is_active': True})
        caner, _ = Person.objects.get_or_create(first_name="Taylor", last_name="Johnson", defaults={'is_active': True})
        rolf, _ = Person.objects.get_or_create(first_name="Casey", last_name="Brown", defaults={'is_active': True})
        lars, _ = Person.objects.get_or_create(first_name="Morgan", last_name="Davis", defaults={'is_active': True})

        # Assign projects
        sandra.projects.add(sfb1368)
        sebastian.projects.add(trr277)
        caner.projects.add(sfb1368, trr277)
        rolf.projects.add(siemens_asg)
        lars.projects.add(siemens_asg)

        # Create presentations
        today = timezone.now().date()
        # Past presentations
        Presentation.objects.get_or_create(
            date=today - timezone.timedelta(days=30),
            presenter=sandra,
            project=sfb1368,
            defaults={'topic': 'Topic 1', 'notes': ''}
        )
        Presentation.objects.get_or_create(
            date=today - timezone.timedelta(days=60),
            presenter=sebastian,
            project=trr277,
            defaults={'topic': 'Topic 2', 'notes': ''}
        )
        # Future presentations
        Presentation.objects.get_or_create(
            date=today + timezone.timedelta(days=7),
            presenter=sandra,
            project=sfb1368,
            defaults={'topic': 'Topic 3', 'notes': ''}
        )
        Presentation.objects.get_or_create(
            date=today + timezone.timedelta(days=14),
            presenter=sebastian,
            project=trr277,
            defaults={'topic': 'Topic 4', 'notes': ''}
        )
        Presentation.objects.get_or_create(
            date=today + timezone.timedelta(days=21),
            presenter=caner,
            project=sfb1368,
            defaults={'topic': 'Topic 5', 'notes': ''}
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded sample data'))