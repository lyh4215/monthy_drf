from django.db import models
from accounts.models import User

# Create your models here.
class Persona(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, related_name='persona')
    persona = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} : {self.persona}'
    
class Nudge(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nudges')
    title = models.CharField(max_length=500)
    pages = models.TextField()
    iconItem = models.CharField(max_length=100)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    #published = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pk}] {self.user}({self.title}): -'
