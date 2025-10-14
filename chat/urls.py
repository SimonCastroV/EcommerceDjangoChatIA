from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path("", views.chat_ui, name="chat_ui"),
    path("api/message/", views.chat_message_api, name="chat_api"),
]
