from django.db import models
from django.contrib.auth.models import User

class LabNotebook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notebook_entries")
    reaction_name = models.CharField(max_length=255)
    reaction_equation = models.TextField()
    explanation = models.TextField()
    animation_url = models.URLField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.reaction_name}"
from django.db import models

# Create your models here.
