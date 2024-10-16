from django.db import models

class News(models.Model):
    english_news = models.JSONField(blank=True, null=True)
    hindi_news = models.JSONField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)