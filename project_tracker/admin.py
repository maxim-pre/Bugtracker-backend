from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse 
from .models import Project, ProjectDeveloper, Ticket, Developer

class TicketInLine(admin.TabularInline):
    model = Ticket
    extra=0
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'creator','date_created', 'tickets_count', 'developers_count'] # column headers in admin interface
    list_editable = ['description'] 
    date_hierarchy = 'date_created'
    list_per_page = 10
    search_fields = ['name']  
    inlines = [TicketInLine]  

    def tickets_count(self, project):
        url = (reverse('admin:project_tracker_ticket_changelist')  
        + '?'
        + urlencode({'project__id': project.id})
        )
        return format_html('<a href="{}">{} tickets</a>', url, project.tickets_count)
    
    def developers_count(self, project):
        url = (reverse('admin:project_tracker_projectdeveloper_changelist')
        + '?'
        + urlencode({'project__id': project.id})
        )
        return format_html('<a href={}>{} developers</a>', url, project.developers_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            tickets_count=Count('ticket')
        ).annotate(
            developers_count=Count('projectdeveloper')
        )
    

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'project_name', 'submitter_name', 'created_at', 'developer_name', 'last_updated', 'status']
    list_select_related = ['project', 'developer', 'submitter'] #the list of fields we want to eager load
    list_filter = ['project', 'created_at']
    list_per_page = 10
    autocomplete_fields = ['project', 'developer', 'submitter']

@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'birthday']
    list_select_related = ['user']
    list_per_page = 10
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name', 'last_name']
    autocomplete_fields = ['user']

@admin.register(ProjectDeveloper)
class ProjectDeveloperAdmin(admin.ModelAdmin):
    list_display = ['developer_name', 'project_title']
    autocomplete_fields = ['project', 'developer']


