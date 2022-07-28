from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models.signals import pre_save
from django.db.models.signals import post_delete
from django.dispatch import receiver


# Create your models here.
class League(models.Model):
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, through='PlayerManager')
    name = models.CharField(max_length=50, null=False)
    slug = models.SlugField(max_length=30, unique=True, null=False)
    # Unique ID for each league
    description = models.TextField()
    date_created = models.DateField(auto_now_add=True)

    GAME_TYPE_OPTIONS = [
        ('01', 'Standard'),
        ('02', 'Standard with Playoffs'),
        ('03', 'Guess that Track'),
    ]
    game_type = models.CharField(max_length=2, default='01', choices=GAME_TYPE_OPTIONS)

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def add_player(self):
        pass

    def add_round(self):
        pass

    def delete_round(self):
        pass


class PlayerManager(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    league = models.ForeignKey(League, related_name="players", on_delete=models.CASCADE, null=True)
    league_admin = models.BooleanField(default=False)

    nickname = models.CharField(max_length=24, null=True, blank=True)
    points = models.SmallIntegerField(default=0)
    profile_img = models.ImageField(upload_to="project/user_profiles/images", blank=True)

    def __str__(self):
        return self.nickname

# When you create a new player, set the nickname as the users username by default
@receiver(pre_save, sender=PlayerManager)
def default_nickname(sender, instance, **kwargs):
    if not instance.nickname:
        instance.nickname = instance.user.username


class Round(models.Model):
    league = models.ForeignKey(League, related_name="rounds", on_delete=models.CASCADE)
    title = models.CharField(max_length=64, null=False)
    description = models.TextField(blank=True)

    ROUND_STATUS_OPTIONS = [
        ('past', 'Expired Round'),
        ('current', 'Current Round'),
        ('future', 'Upcoming Round'),
    ]
    status = models.CharField(max_length=7, default='future', choices=ROUND_STATUS_OPTIONS)

    def __str__(self):
        return self.title

    def add_song(self, link):
        # if you havent submitted
        # s = Song(round=self, submitter=User, link=link)
        # s.save()
        pass

    def change_song(self):
        # if the deadline hasnt passed, allow this
        pass


class Song(models.Model):
    round = models.ForeignKey(Round, related_name="songs", on_delete=models.CASCADE)
    league = models.ForeignKey(Round, on_delete=models.CASCADE)
    submitter = models.ForeignKey(PlayerManager, on_delete=models.CASCADE)
    link = models.CharField(max_length=80)
    name = models.CharField(max_length=40, blank=True)
    artist = models.CharField(max_length=40, blank=True)
    album_cover_url = models.CharField(max_length=40, blank=True)
    points = models.SmallIntegerField(default=0)

    def __str__(self):
        pass
        # return self.name


# @receiver(post_delete, sender=Screenshot)
# def delete_s3_bucket_file(sender, instance, using, **kwargs):
#     instance.image.delete(save=False)
