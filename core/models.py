from django.db import models
from django.conf import settings
# Create your models here.
class Expert(models.Model):
    name = models.CharField(max_length=45)
    email = models.EmailField(max_length=45)
    description = models.CharField(max_length=500)
    contact = models.CharField(max_length=20)
    token = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class Event(models.Model):
    date = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(max_length=128)
    scheduled = models.BooleanField(default=False)
    expert = models.ForeignKey("Expert",
                               on_delete=models.SET_NULL,
                               null=True,
                               related_name="expert_events")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL,
                             null=True,
                             related_name="user_events")

    def __str__(self):
        return "Session with " + self.expert.name
