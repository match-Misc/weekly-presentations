from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    CATEGORY_CHOICES = [
        ('RES', 'Research (SFB/TRR/SPP)'),
        ('IND', 'Industrieprojekt'),
        ('MSC', 'Sonstiges'),
    ]
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES, default='RES')

    def __str__(self):
        return self.name

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    projects = models.ManyToManyField(Project, related_name='members', blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Presentation(models.Model):
    date = models.DateField()
    time = models.TimeField(default='09:00:00')
    presenter = models.ForeignKey(Person, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    topic = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)

    @property
    def kw(self):
        return self.date.isocalendar()[1]

    def __str__(self):
        return f"{self.date} - {self.presenter}"
