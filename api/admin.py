from django.contrib import admin
from .models import Tick
# Register your models here.

class TickAdmin(admin.ModelAdmin):
	pass

admin.site.register(Tick, TickAdmin)