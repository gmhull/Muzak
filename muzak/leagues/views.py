from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.conf import settings
from django.forms import formset_factory
from .models import League, Round, PlayerManager, Song
from .forms import SongSubmissionForm, VotingForm

# Create your views here.
class LeagueDetailView(DetailView):
    model = League
    template_name = 'leagues/league_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['round_list'] = Round.objects.filter(league=self.object)

        player = PlayerManager.objects.filter(user=self.request.user).filter(league=self.object).get()
        context['rounds_user_submitted_in'] = Round.objects.filter(league=self.object).filter(songs__submitter=player)
        return context


class LeagueListView(ListView):
    model = League
    ordering = ["-date_created"]
    template_name = 'leagues/leagues_home.html'

    def get_queryset(self):
        return League.objects.filter(player=self.request.user)


class LeagueStandingsListView(DetailView):
    model = League
    template_name = 'leagues/league_standings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['player_list'] = PlayerManager.objects.filter(league=self.object).order_by('-points')
        return context


class RoundResultsListView(DetailView):
    model = Round
    template_name = 'leagues/round_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['song_list'] = Song.objects.filter(round=self.object).order_by('-points')
        return context


@login_required
def league_standings(request):
    return render(request, 'leagues/league_standings.html')

@login_required
def league_round(request, slug, pk):
    return render(request, 'leagues/round_detail.html')

@login_required
def round_voting(request, slug, pk):
    round = Round.objects.get(id=pk)
    context = {}
    player = PlayerManager.objects.filter(user=request.user).filter(league=round.league).get()
    songs_list = Song.objects.filter(round=round)
    context['player'] = player
    context['songs_list'] = songs_list

    VotingFormSet = formset_factory(VotingForm, extra=len(songs_list))
    formset = VotingFormSet()
    context['formset'] = formset
    context['song_forms'] = zip(songs_list, formset)

    if request.method == 'GET':
        return render(request, 'leagues/round_voting.html', context)

    if request.method == 'POST':
        formset = VotingFormSet(request.POST)
        print(request.POST)
        if formset.is_valid():
            print("Form is valid")
            for form in formset:
                if form.cleaned_data['vote'] == '':
                    form.cleaned_data['vote'] = 0
                vote_cast = round.cast_vote(player,
                                            form.cleaned_data['song'],
                                            form.cleaned_data['vote'],
                                            form.cleaned_data['message'])

            return redirect('round_results', round.league.slug, round.pk)
        else:
            print("Form not valid")
            return render(request, 'leagues/round_voting.html', context)

@login_required
def song_submission(request, slug, pk):
    round = Round.objects.get(id=pk)
    player = PlayerManager.objects.filter(user=request.user).filter(league=round.league).get()
    try:
        song_submitted = Song.objects.filter(round=round).filter(submitter=player).get()
    except:
        song_submitted = ""

    if request.method == 'GET':
        form = SongSubmissionForm()
        return render(request, 'leagues/song_submission.html', {"round": round, "song_submitted": song_submitted, "form": form})

    if request.method == 'POST':
        form = SongSubmissionForm(request.POST)
        link = request.POST['link']
        valid_song = False
        if form['type'].value() == 'new_song':
            valid_song = round.add_song(link, player)
            valid_song = True
        elif form['type'].value() == 'change_song':
            valid_song = round.change_song(link, song_submitted)
            valid_song = True

        if valid_song:
            song_submitted = Song.objects.filter(round=round).filter(submitter=player).get()
            return render(request, 'leagues/song_submission.html', {"round": round, "song_submitted": song_submitted, "post": True})
        else:
            return render(request, 'leagues/song_submission.html', {"round": round, "song_submitted": song_submitted})
