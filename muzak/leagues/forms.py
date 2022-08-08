from django import forms
from .models import Song, Round, PlayerManager, Vote
from django.conf import settings
from django.core.exceptions import ValidationError


class SongSubmissionForm(forms.Form):
    type = forms.CharField(label='Update Type', max_length=100, required=False)
    link = forms.CharField(label='Song Link', max_length=100, required=False)
    name = forms.CharField(label='Song Name', max_length=100, required=False)
    artist = forms.CharField(label='Song Artist', max_length=100, required=False)
    album_cover_url = forms.CharField(label='Album Cover URL', max_length=100, required=False)

class VotingForm(forms.Form):
    submitter = forms.CharField(max_length=60)
    song = forms.CharField(max_length=60)
    vote = forms.IntegerField(label="Vote Total", max_value=10, min_value=-10)
    message = forms.CharField(label='Voting Message', max_length=200, required=False)

    def clean(self):
        cd = self.cleaned_data

        song = Song.objects.get(id=cd.get("song"))
        round = song.round
        submitter = PlayerManager.objects.get(user_id=int(cd.get("submitter")), league=song.league)

        # Confirm that there is a unique vote cast for each song
        for instance in Vote.objects.filter(target_song=song, round=round, submitter=submitter).all():
            if instance:
                print('duplicate vote')
                raise ValidationError("This is a duplicate vote")
            print('clean')

        # Confirm that a user did not vote for their own song
        for instance in Vote.objects.filter(target_song__submitter=submitter, submitter=submitter).all():
            if instance:
                print('self vote')
                raise ValidationError("Player voted for themselves")

        return cd
