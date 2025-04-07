from django.contrib import admin
from .models import Devices, Temperatures, Pressures, Altitudes

@admin.register(Devices)
class DevicesAdmin(admin.ModelAdmin):
    list_display = ('uid', 'name', 'description', 'lastSeenAt')
    search_fields = ('uid', 'name')
    list_editable = ('description',) 

admin.site.register(Temperatures)
admin.site.register(Pressures)
admin.site.register(Altitudes)