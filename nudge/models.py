from django.db import models
from accounts.models import User

# Create your models here.
class Persona(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    persona = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} : {self.persona}'
    
class Nudge(models.Model):

    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    #published = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pk}] {self.user}({self.date}): -'
