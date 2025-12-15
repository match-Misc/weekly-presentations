from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Max
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm, ChoiceField
from icalendar import Calendar, Event
import pytz
from datetime import timedelta
from .models import Presentation, Project, Person

def get_next_tuesdays(n=16):
    today = timezone.now().date()
    # Find next Tuesday (weekday 1)
    days_ahead = (1 - today.weekday() + 7) % 7
    if days_ahead == 0:
        days_ahead = 7
    next_tue = today + timedelta(days=days_ahead)
    tuesdays = [next_tue + timedelta(weeks=i) for i in range(n)]
    return tuesdays

class PresentationForm(ModelForm):
    class Meta:
        model = Presentation
        fields = ['date', 'time', 'presenter', 'project', 'topic', 'notes']

def home(request):
    today = timezone.now().date()
    presentations = Presentation.objects.filter(date__gte=today, presenter__is_active=True).order_by('date')
    next_presentation = presentations.first() if presentations else None
    for presentation in presentations:
        days = (presentation.date - today).days
        if days <= 14:
            presentation.status_class = 'status-yellow'
        else:
            presentation.status_class = 'status-green'
    return render(request, 'schedule/home.html', {
        'presentations': presentations,
        'next_presentation': next_presentation,
    })

def projects(request):
    projects = Project.objects.prefetch_related('members__presentation_set').all()
    today = timezone.now().date()
    for project in projects:
        last_dates = []
        past_presentations = []
        for member in project.members.all():
            presentations = member.presentation_set.filter(project=project)
            for pres in presentations:
                if pres.date < today:
                    past_presentations.append(pres)
                last = presentations.aggregate(Max('date'))['date__max']
                if last:
                    last_dates.append(last)
        project.last_presentation_date = max(last_dates) if last_dates else None
        project.past_presentations = sorted(past_presentations, key=lambda x: x.date, reverse=True)[:5]  # Last 5
    return render(request, 'schedule/projects.html', {'projects': projects})

def people(request):
    people = Person.objects.filter(is_active=True).prefetch_related('presentation_set', 'projects')
    people_data = []
    today = timezone.now().date()
    for person in people:
        presentations = person.presentation_set.order_by('-date')
        last_presentation = presentations.first()
        last_date = last_presentation.date if last_presentation else None
        past_presentations = presentations.filter(date__lt=today)[:5]  # Last 5 past
        people_data.append({
            'person': person,
            'last_presentation_date': last_date,
            'future_presentations': presentations.filter(date__gte=today),
            'past_presentations': past_presentations,
        })
    return render(request, 'schedule/people.html', {'people_data': people_data})

def download_ics(request, pk):
    from django.shortcuts import get_object_or_404
    pres = get_object_or_404(Presentation, pk=pk, presenter__is_active=True)
    berlin_tz = pytz.timezone('Europe/Berlin')

    cal = Calendar()
    cal.add('prodid', '-//Meeting Scheduler//')
    cal.add('version', '2.0')

    event = Event()
    dt = timezone.datetime.combine(pres.date, pres.time)
    dt_berlin = berlin_tz.localize(dt)
    event.add('dtstart', dt_berlin)
    event.add('dtend', dt_berlin + timezone.timedelta(hours=1))  # Assume 1 hour duration
    event.add('summary', pres.topic or 'Presentation')
    desc = f"Presenter: {pres.presenter}\nProject: {pres.project or 'N/A'}\nNotes: {pres.notes}"
    event.add('description', desc)
    event.add('location', 'Meeting Room')
    cal.add_component(event)

    response = HttpResponse(cal.to_ical(), content_type='text/calendar')
    response['Content-Disposition'] = f'attachment; filename="meeting_{pres.date}_{pres.presenter}.ics"'
    return response

@login_required
def schedule(request):
    persons = Person.objects.filter(is_active=True).annotate(last_pres=Max('presentation__date')).order_by('last_pres')
    projects = Project.objects.annotate(last_pres=Max('presentation__date')).order_by('last_pres')
    tuesdays = get_next_tuesdays()
    if request.method == 'POST':
        form = PresentationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('schedule')
    else:
        initial = {}
        if 'presenter' in request.GET:
            initial['presenter'] = request.GET['presenter']
        if 'project' in request.GET:
            initial['project'] = request.GET['project']
        form = PresentationForm(initial=initial)
    form.fields['date'] = ChoiceField(choices=[(d, d.strftime('%d.%m.%Y')) for d in tuesdays], label='Date')
    form.fields['presenter'].queryset = persons
    form.fields['project'].queryset = projects
    return render(request, 'schedule/schedule.html', {
        'persons': persons,
        'projects': projects,
        'form': form,
    })
