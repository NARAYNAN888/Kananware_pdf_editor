from django.contrib import admin
from .models import SupportRequest
# Register your models here.

@admin.register(SupportRequest)
class SupportRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "mobile", "created_at")
    search_fields = ("name", "email", "mobile")
