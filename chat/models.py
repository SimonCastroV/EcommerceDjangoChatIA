from django.db import models

class ChatMessage(models.Model):
    SESSION_ROLE = (('user','user'),('assistant','assistant'))
    session_id = models.CharField(max_length=100, db_index=True)
    role = models.CharField(max_length=20, choices=SESSION_ROLE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.session_id} - {self.role}: {self.message[:30]}"
