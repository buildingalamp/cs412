# File: views.py
# Author: Jeffrey Zhou (jzhou25@bu.edu), 6/15/2025
# Description: views file used to define the view classes

from django.shortcuts import render
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Voter
from datetime import date
import plotly
import plotly.graph_objs as go
from django.db.models import Count


# Create your views here.

class VoterListView(ListView):
    """View to display voter data"""

    model = Voter
    template_name = "voter_analytics/voters.html"
    context_object_name = "voters"
    paginate_by = 100 # how many voters per page


    def get_queryset(self):
        """Method to handle filtering voters from search"""

        # start with entire queryset
        voters = super().get_queryset()

        # filter by party affiliation:
        if 'party_affiliation' in self.request.GET:
            party_affiliation = self.request.GET['party_affiliation']
            if party_affiliation:
                voters = voters.filter(party_affiliation=party_affiliation)
        
        # filter by voter score:
        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if voter_score:
                voters = voters.filter(voter_score=voter_score)

        # filter by min date of birth:
        if 'min_dob' in self.request.GET:
            min_dob = self.request.GET['min_dob']
            if min_dob:
                min_dob_date = date(int(min_dob), 1, 1)
                voters = voters.filter(date_of_birth__gte=min_dob_date)

        # filter by max date of birth:
        if 'max_dob' in self.request.GET:
            max_dob = self.request.GET['max_dob']
            if max_dob:
                max_dob_date = date(int(max_dob), 1, 1)
                voters = voters.filter(date_of_birth__lte=max_dob_date)

        # filter by max date of birth:
        if 'max_dob' in self.request.GET:
            max_dob = self.request.GET['max_dob']
            if max_dob:
                voters = voters.filter(voter_score__lte=max_dob)
                
        for field in ["v20state", "v21town", "v21primary", "v22general", "v23town"]:
            if field in self.request.GET:
                kwargs = {field: True}
                voters = voters.filter(**kwargs)

        return voters
    
    def get_context_data(self, **kwargs):
        """Method to provide form fields for search"""

        context = super().get_context_data(**kwargs)

        # form fields
        context["party_affiliations"] = ['U ', 'D ', 'R ', 'J ', 'A ', 'CC',
                                         'X ', 'L ', 'Q ', 'S ', 'FF', 'G ',
                                        'HH', 'T ', 'AA', 'GG', 'Z ', 'O ', 
                                        'P ', 'E ', 'V ', 'H ', 'Y ', 'W ', 
                                        'EE', 'K ']
        context["voter_scores"] = range(0, 6)
        context["years"] = range(1920, 2005)
        context["voted_in"] = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']

        return context
    
class VoterDetailView(DetailView):
    """Display data for a single voter"""

    model = Voter
    context_object_name = 'v'
    template_name = 'voter_analytics/voter_detail.html'

class VoterGraphView(ListView):
    """Display graphs for voter data"""

    model = Voter
    context_object_name = 'voters'
    template_name = 'voter_analytics/graphs.html'

    def get_queryset(self):
        """Method to handle filtering voters from search"""

        # start with entire queryset
        voters = super().get_queryset()

        # filter by party affiliation:
        if 'party_affiliation' in self.request.GET:
            party_affiliation = self.request.GET['party_affiliation']
            if party_affiliation:
                voters = voters.filter(party_affiliation=party_affiliation)
        
        # filter by voter score:
        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if voter_score:
                voters = voters.filter(voter_score=voter_score)

        # filter by min date of birth:
        if 'min_dob' in self.request.GET:
            min_dob = self.request.GET['min_dob']
            if min_dob:
                min_dob_date = date(int(min_dob), 1, 1)
                voters = voters.filter(date_of_birth__gte=min_dob_date)

        # filter by max date of birth:
        if 'max_dob' in self.request.GET:
            max_dob = self.request.GET['max_dob']
            if max_dob:
                max_dob_date = date(int(max_dob), 1, 1)
                voters = voters.filter(date_of_birth__lte=max_dob_date)

        # filter by max date of birth:
        if 'max_dob' in self.request.GET:
            max_dob = self.request.GET['max_dob']
            if max_dob:
                voters = voters.filter(voter_score__lte=max_dob)
                
        for field in ["v20state", "v21town", "v21primary", "v22general", "v23town"]:
            if field in self.request.GET:
                kwargs = {field: True}
                voters = voters.filter(**kwargs)

        return voters

    def get_context_data(self, **kwargs):
        """Method to handle creating graphs from data, and to provide fields for search form"""

        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()

        # By year of birth
        dob_data = voters.values_list('date_of_birth', flat=True)
        years = [dob.year for dob in dob_data if dob is not None]
        year_counts = {}
        for year in years:
            year_counts[year] = year_counts.get(year, 0) + 1

        histogram_by_year = go.Figure(data=[go.Bar(x=list(year_counts.keys()), y=list(year_counts.values()))])
        context['birth_year_hist'] = plotly.offline.plot(histogram_by_year, output_type='div')

        # By party affiliation
        party_data = voters.values('party_affiliation').annotate(count=Count('party_affiliation'))
        labels = [entry['party_affiliation'] or 'None' for entry in party_data]
        values = [entry['count'] for entry in party_data]

        pie_party = go.Figure(data=[go.Pie(labels=labels, values=values)])
        context['party_pie'] = plotly.offline.plot(pie_party, output_type='div')

        # By participation in elections
        elections = ["v20state", "v21town", "v21primary", "v22general", "v23town"]
        participation = {
            field: voters.filter(**{field: True}).count()
            for field in elections
        }
        election_hist = go.Figure(data=[go.Bar(x=list(participation.keys()), y=list(participation.values()))])
        context['election_hist'] = plotly.offline.plot(election_hist, output_type='div')

        # Add form support variables
        context["party_affiliations"] = ['U ', 'D ', 'R ', 'J ', 'A ', 'CC',
                                         'X ', 'L ', 'Q ', 'S ', 'FF', 'G ',
                                        'HH', 'T ', 'AA', 'GG', 'Z ', 'O ', 
                                        'P ', 'E ', 'V ', 'H ', 'Y ', 'W ', 
                                        'EE', 'K ']
        context["voter_scores"] = range(0, 6)
        context["years"] = range(1920, 2005)

        return context
