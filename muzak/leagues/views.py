from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import League, Round
from django.conf import settings

# Create your views here.
class LeagueDetailView(DetailView):
    model = League
    template_name = 'leagues/league_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['round_list'] = Round.objects.filter(league=self.object)
        return context


class LeagueListView(ListView):
    model = League
    ordering = ["-date_created"]
    template_name = 'leagues/leagues_home.html'

    def get_queryset(self):
        return League.objects.filter(user=self.request.user)


class RoundListView(ListView):
    model = Round
    ordering = ["-pk"]
    template_name = 'leagues/league_detail.html'

    def get_queryset(self):
        return Round.objects.filter(league=Round.league)


@login_required
def league_standings(request):
    return render(request, 'leagues/league_standings.html')

@login_required
def league_round(request):
    return render(request, 'leagues/round_detail.html')

@login_required
def round_voting(request):
    return render(request, 'leagues/round_voting.html')

@login_required
def round_results(request):
    return render(request, 'leagues/round_results.html')
