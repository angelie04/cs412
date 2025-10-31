from django.shortcuts import render
from django.db.models.query import QuerySet
from django.views.generic import *
from . models import Voter
#import plotly library for graphing
import plotly
import plotly.graph_objs as go
from collections import Counter


# Create your views here.

class VoterListView(ListView):
    """View to display Voter results"""
    model = Voter
    template_name = "voter_analytics/voters.html"
    context_object_name = "voters"
    paginate_by = 100

    def get_queryset(self):
        """Override the default queryset to allow for filtering.
        """
        results = super().get_queryset()
        req = self.request.GET

        # Party affiliation (strip trailing space and match case-insensitive)
        party = req.get('party_affiliation')
        if party:
            results = results.filter(party_affiliation=party)
        
        # Voter score (exact match)
        score = req.get('voter_score')
        if score:
            try:
                results = results.filter(voter_score=int(score))
            except ValueError:
                # ignore invalid input
                pass

        # DOB year range
        min_year = req.get('min_year')
        if min_year:
            try:
                results = results.filter(dob__year__gte=int(min_year))
            except ValueError:
                pass
        max_year = req.get('max_year')
        if max_year:
            try:
                results = results.filter(dob__year__lte=int(max_year))
            except ValueError:
                pass

        # Election participation checkboxes: require True when present
        for field in ('v20state', 'v21town', 'v21primary', 'v22general', 'v23town'):
            if req.get(field):
                results = results.filter(**{field: True})

        return results

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        req = self.request.GET
        # copy GET params and remove page so we can append a new page param
        q = self.request.GET.copy()
        if 'page' in q:
            q.pop('page')
        context['querystring'] = q.urlencode()

        # define a list of possible party affiliations from the DB
        parties = { (p or '') for p in Voter.objects.values_list('party_affiliation', flat=True) }
        parties = sorted([p for p in parties if p])
        context['party_affiliation'] = parties
        
        # fixed DOB year range 1940..2004 (descending)
        context['years'] = list(range(1920, 2005))

        # voter score choices 0..5
        context['score_choices'] = list(range(0, 6))

        # Election participation checkboxes
        context['election_choices'] = [
            'v20state', 'v21town', 'v21primary', 'v22general', 'v23town'
        ] 
        return context
        

class VoterDetailView(DetailView):
    """View to display details of a single Voter"""
    model = Voter
    template_name = "voter_analytics/voter_detail.html"
    context_object_name = "voter"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # build a simple address string for mapping; adjust field names if yours differ
        parts = [
            str(getattr(self.object, 'street_number', '') or '').strip(),
            getattr(self.object, 'street_name', '') or '',
            (f"Apt {self.object.apartment}" if getattr(self.object, 'apartment', None) else ''),
            getattr(self.object, 'zip_code', '') or ''
        ]
        addr = " ".join(p for p in parts if p)
        context['map_query'] = addr

        return context

class VoterGraphView(ListView):
    """View to display a graph of Voter data"""
    model = Voter
    template_name = "voter_analytics/graphs.html"
    context_object_name = "graphs"


    def get_queryset(self):
        """Override the default queryset to allow for filtering.
        """
        results = super().get_queryset()
        req = self.request.GET

        # Party affiliation (strip trailing space and match case-insensitive)
        party = req.get('party_affiliation')
        if party:
            results = results.filter(party_affiliation=party)
        
        # Voter score (exact match)
        score = req.get('voter_score')
        if score:
            try:
                results = results.filter(voter_score=int(score))
            except ValueError:
                # ignore invalid input
                pass

        # DOB year range
        min_year = req.get('min_year')
        if min_year:
            try:
                results = results.filter(dob__year__gte=int(min_year))
            except ValueError:
                pass
        max_year = req.get('max_year')
        if max_year:
            try:
                results = results.filter(dob__year__lte=int(max_year))
            except ValueError:
                pass

        # Election participation checkboxes: require True when present
        for field in ('v20state', 'v21town', 'v21primary', 'v22general', 'v23town'):
            if req.get(field):
                results = results.filter(**{field: True})

        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        querys = self.get_queryset()
        # define a list of possible party affiliations from the DB
        parties = { (p or '') for p in Voter.objects.values_list('party_affiliation', flat=True) }
        parties = sorted([p for p in parties if p])
        context['party_affiliation'] = parties

        # fixed DOB year range 1940..2004 (descending)
        context['years'] = list(range(1920, 2005))

        # voter score choices 0..5
        context['score_choices'] = list(range(0, 6))

        # Election participation checkboxes
        context['election_choices'] = [
            'v20state', 'v21town', 'v21primary', 'v22general', 'v23town'
        ] 
        # create a graph of voter distribution by year of birth
        # apply filter list of voters and then apply that to my graph
        # dob_values = Voter.objects.values_list('dob', flat=True)
        dob_values = querys.values_list('dob', flat=True)
        years_list = [d.year for d in dob_values if d]

        counts = Counter(years_list)
        year = list(range(1920, 2005))
        voter_count = [counts.get(y, 0) for y in year]

        fig = go.Bar(x = year, y = voter_count)
        title_text = "Voter Distribution by Year of Birth"
        graph_year = plotly.offline.plot({
            "data": [fig],
            "layout_title_text": title_text,
            "layout_xaxis_title": "Year of Birth",
            "layout_yaxis_title": "Number of Voters",
        }, auto_open=False, output_type='div')

        context['graph_year'] = graph_year

        # graph for distribution of Voters by their party affiliation
        labels = parties
        values = [querys.filter(party_affiliation=p).count() for p in parties]
        fig = go.Pie(labels=labels, values=values)
        title_text = "Voter Distribution by Party Affiliation"

        graph_party = plotly.offline.plot({
            "data": [fig],
            "layout_title_text": title_text,
        }, auto_open=False, output_type='div')

        context['graph_party'] = graph_party

        # bar chart for distribution of Voters by their participation in each of the 5 elections
        x_axis = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        y_axis = [querys.filter(**{e: True}).count() for e in x_axis]
        fig = go.Bar(x =x_axis, y =y_axis)
        title_text = "Voter Count by Election"

        graph_election = plotly.offline.plot({
            "data": [fig],
            "layout_title_text": title_text,
        }, auto_open=False, output_type='div')
        context['graph_election'] = graph_election

        return context