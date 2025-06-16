from django.shortcuts import render
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Voter
from datetime import date


# Create your views here.

class VoterListView(ListView):
    """View to display voter data"""

    model = Voter
    template_name = "voter_analytics/voters.html"
    context_object_name = "voters"
    paginate_by = 100 # how many voters per page


    def get_queryset(self):

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
                queryset = voters.filter(**kwargs)

        return voters
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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