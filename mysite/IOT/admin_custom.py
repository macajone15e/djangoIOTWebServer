from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from .models import Devices, Temperatures, Pressures, Altitudes

from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

class IOTAdminSite(AdminSite):
    site_header = "IOT Administration"
    site_title = "IOT Admin"
    index_title = "Tableau de bord"

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)
        for app in app_list:
            if app["app_label"] == "IOT":
                app["models"].sort(key=lambda x: [
                    "Devices", "Temperatures", "Pressures", "Altitudes"
                ].index(x["object_name"]))
        return app_list

# Crée une instance de ton admin personnalisé
admin_site = IOTAdminSite(name='iotadmin')

# Enregistre les modèles IOT
admin_site.register(Devices)
admin_site.register(Temperatures)
admin_site.register(Pressures)
admin_site.register(Altitudes)

# Enregistre les Users & Groups avec leurs admin personnalisés natifs
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
