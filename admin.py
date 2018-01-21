from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from geofence.models import Driver,Geofence, Vehicle, History, Child, Company

# class DriverAdmin(admin.Admin):
#     actions = [give_permission]
admin.site.register(Driver)
admin.site.register(Geofence)
admin.site.register(Vehicle)
admin.site.register(History)
admin.site.register(Child)
admin.site.register(Company)
