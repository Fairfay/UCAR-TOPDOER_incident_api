from django.contrib import admin

from incident.models import Incident


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'description_short',
        'status', 'source',
        'created_at', 'updated_at'
    )
    list_filter = (
        'status', 'source',
        'created_at'
    )
    search_fields = (
        'description',
    )
    readonly_fields = (
        'created_at', 'updated_at'
    )
    list_editable = (
        'status',
    )

    @admin.display(
        description="Описание (кратко)",
        ordering="description"
    )
    def description_short(self, obj):
        return obj.description[:75]
