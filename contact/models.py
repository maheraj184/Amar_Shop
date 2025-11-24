from django.db import models

class GroupMember(models.Model):
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    linkedin = models.URLField(blank=True)

    def __str__(self):
        return self.name