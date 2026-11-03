from django.contrib import admin
from .models import Logs

class LOG_ADMIN(admin.ModelAdmin):
    search_fields = ['username','writer','tarikh','level','ip','method','route']
    list_filter = ['level','writer']
    list_display = ['level','tarikh','writer','username','ip','method','route']

admin.site.register(Logs , LOG_ADMIN)