from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('session_id','role','created_at')
    list_filter = ('role','session_id')
