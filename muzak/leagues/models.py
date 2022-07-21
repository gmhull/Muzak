from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver


# Create your models here.
class League(models.Model):
    name = models.CharField(max_length=50, null=False)
    # Unique ID for each league
    # id = models.CharField(max_length=10, unique=True, null=False)
    description = models.TextField()

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


class Player(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    league = models.ForeignKey(League, related_name="players", on_delete=models.CASCADE, null=True)

    nickname = models.CharField(max_length=24, null=True, blank=True)
    points = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.nickname

# When you create a new player, set the nickname as the users username by default
@receiver(pre_save, sender=Player)
def default_nickname(sender, instance, **kwargs):
     if not instance.nickname:
         instance.nickname = instance.user.username


class Round(models.Model):
    league = models.ForeignKey(League, related_name="rounds", on_delete=models.CASCADE)
    title = models.CharField(max_length=64, null=False)
    description = models.TextField(blank=True)

    # songs = models.ManyToManyField(Song, through='Player')

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
    submitter = models.ForeignKey(Player, on_delete=models.CASCADE)
    link = models.CharField(max_length=80)
    # name =
    # artist =
    # album_cover =
    points = models.SmallIntegerField(default=0)

    def __str__(self):
        pass
        # return self.name
