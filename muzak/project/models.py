from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class MuzakUser(AbstractUser):
    profile_img = models.ImageField(upload_to="project/user_profiles/images", blank=True)

    def __str__(self):
        return self.username
