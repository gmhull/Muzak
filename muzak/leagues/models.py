from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models.signals import pre_save, post_delete
from django.db.models import Sum
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# Create your models here.
class League(models.Model):
    player = models.ManyToManyField(settings.AUTH_USER_MODEL, through='PlayerManager')
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

    class Meta:
        db_table = 'leagues_playermanager'
        constraints = [
            models.UniqueConstraint(fields=['user', 'league'], name='unique player'),
        ]


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
        ('voting', 'Currently Voting'),
        ('submitting', 'Currently Submitting'),
        ('future', 'Upcoming Round'),
    ]
    status = models.CharField(max_length=7, default='future', choices=ROUND_STATUS_OPTIONS)

    def __str__(self):
        return self.title

    def add_song(self, link, player):
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        track = sp.track(link)
        if track:
            s = Song(round=self, submitter=player, link=link,
                     name=track['name'],
                     artist=track['artists'][0]['name'],
                     album_cover_url=track['album']['name'])
            s.save()
            return True

        return False

    def change_song(self, link, song):
        # if the deadline hasnt passed, allow this
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        track = sp.track(link)
        if track:
            Song.objects.filter(id=song.id).update(link=link)
            Song.objects.filter(id=song.id).update(name=track['name'])
            Song.objects.filter(id=song.id).update(artist=track['artists'][0]['name'])
            Song.objects.filter(id=song.id).update(album_cover_url=track['album']['images'][1]['url'])
            return True

        return False

    def cast_vote(self, player, song, points, message):
        song = Song.objects.get(id=song, round=self)
        try:
            vote = Vote(round=self, submitter=player,
                        target_song=song, points=points, message=message)
            vote.save()

            # Update the points associated with each song every time someone votes
            self.update_points()

            return True
        except:
            return False

    def update_points(self):
        print("Updating")
        for song in Song.objects.filter(round=self).all():
            points = Vote.objects.filter(target_song=song).aggregate(Sum('points'))['points__sum']
            Song.objects.filter(id=song.id).update(points=points)


class Song(models.Model):
    round = models.ForeignKey(Round, related_name="songs", on_delete=models.CASCADE)
    league = models.ForeignKey(League, related_name="songs", on_delete=models.CASCADE)
    submitter = models.ForeignKey(PlayerManager, on_delete=models.CASCADE)
    link = models.CharField(max_length=80)
    name = models.CharField(max_length=60)
    artist = models.CharField(max_length=40, blank=True)
    album_cover_url = models.CharField(max_length=100, blank=True)
    points = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'leagues_song'
        constraints = [
            models.UniqueConstraint(fields=['round', 'submitter'], name='one song per player'),
            models.UniqueConstraint(fields=['round', 'link'], name='unique song in round'),
        ]


# When you create a new song, set the league to the same as the rounds league
@receiver(pre_save, sender=Song)
def default_nickname(sender, instance, **kwargs):
    instance.league = instance.round.league


class Vote(models.Model):
    round = models.ForeignKey(Round, related_name="votes", on_delete=models.CASCADE)
    submitter = models.ForeignKey(PlayerManager, on_delete=models.CASCADE)
    target_song = models.ForeignKey(Song, related_name="votes", on_delete=models.CASCADE)
    points = models.SmallIntegerField(default=0)
    message = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'leagues_vote'
        constraints = [
            models.UniqueConstraint(fields=['round', 'submitter', 'target_song'], name='one vote per song, per player'),
        ]
