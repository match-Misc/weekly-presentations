from django.contrib import admin
from django.http import HttpResponse
from django.conf import settings
import os
import shutil
import tempfile
from datetime import datetime
from .models import Project, Person, Presentation

class ProjectInline(admin.TabularInline):
    model = Person.projects.through
    extra = 1

class PersonAdmin(admin.ModelAdmin):
    inlines = [ProjectInline]
    list_display = ['first_name', 'last_name', 'is_active']
    list_filter = ['is_active', 'projects']

class PresentationAdmin(admin.ModelAdmin):
    list_display = ['date', 'time', 'kw', 'presenter', 'project', 'topic', 'is_completed']
    list_filter = ['date', 'project', 'is_completed']
    search_fields = ['presenter__first_name', 'presenter__last_name', 'topic']

def backup_database(request):
    db_path = settings.DATABASES['default']['NAME']
    if not os.path.exists(db_path):
        return HttpResponse("Database not found", status=404)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.sqlite3') as tmp:
        shutil.copy(db_path, tmp.name)
        with open(tmp.name, 'rb') as f:
            data = f.read()
        os.unlink(tmp.name)
        response = HttpResponse(data, content_type='application/octet-stream')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        response['Content-Disposition'] = f'attachment; filename="db_backup_{timestamp}.sqlite3"'
        return response

admin.site.register(Project)
admin.site.register(Person, PersonAdmin)
admin.site.register(Presentation, PresentationAdmin)
# admin.site.register_view('backup/', backup_database, name='backup_database')  # Deprecated in Django, use custom URLs instead
