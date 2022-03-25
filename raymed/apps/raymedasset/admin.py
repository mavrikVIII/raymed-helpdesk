from django.contrib import admin
from .models import Device, Person, Subdevice, HistoryMoveDevice
admin.site.register(Device)
admin.site.register(Person)
admin.site.register(Subdevice)
admin.site.register(HistoryMoveDevice)
