# File: voter_analytics/views.py
# Author: Saksham Goel (sakshamg@bu.edu), 10/28/2025
# Description: Views for the voter_analytics application, including voters and graphs views.

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
import re
import plotly
import plotly.graph_objs as go
from collections import Counter


def _extract_year(dob_text):
	"""Try to extract a 4-digit year from a text DOB field.

	Returns int year or None.
	"""
	if not dob_text:
		return None
	m = re.search(r"(\d{4})", dob_text)
	if m:
		try:
			return int(m.group(1))
		except:
			return None
	return None


class VoterListView(ListView):
	"""View to display list of voters"""
	model = Voter
	template_name = 'voter_analytics/voters.html'
	context_object_name = 'voters'
	paginate_by = 100

	def get_queryset(self):
		"""Get the queryset of voters."""
		qs = Voter.objects.all()

		# apply simple filters that can be done in the DB
		party = self.request.GET.get('party')
		if party:
			qs = qs.filter(party=party)

		score = self.request.GET.get('voter_score')
		if score and score.isdigit():
			qs = qs.filter(voter_score=int(score))

		# election flags: if present and value is 'on' filter v==1
		elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
		for e in elections:
			if self.request.GET.get(e) == 'on':
				qs = qs.filter(**{e: 1})

		# date-of-birth year min/max need parsing of text field; do in Python
		min_year = self.request.GET.get('min_dob')
		max_year = self.request.GET.get('max_dob')

		if min_year or max_year:
			min_y = int(min_year) if (min_year and min_year.isdigit()) else None
			max_y = int(max_year) if (max_year and max_year.isdigit()) else None

			# convert queryset to list and filter by extracted year
			filtered = []
			for v in qs:
				y = _extract_year(v.date_of_birth)
				if y is None:
					continue
				if min_y and y < min_y:
					continue
				if max_y and y > max_y:
					continue
				filtered.append(v)
			return filtered

		return qs

	def get_context_data(self, **kwargs):
		"""Get the context data for the voter list view. 
		Includes choices for filters (party, year of birth, 
		voter score) and query params for navigation links."""
		ctx = super().get_context_data(**kwargs)

		# choices for filters
		ctx['parties'] = Voter.objects.values_list('party', flat=True).distinct().order_by('party')
		# derive years from DOBs
		years = set()
		for dob in Voter.objects.values_list('date_of_birth', flat=True):
			y = _extract_year(dob)
			if y:
				years.add(y)
		ctx['years'] = sorted(years)

		# voter_score choices
		ctx['scores'] = Voter.objects.values_list('voter_score', flat=True).distinct().order_by('-voter_score')

		# keep query params for navigation links
		ctx['querystring'] = '&'.join([f"{k}={v}" for k, v in self.request.GET.items() if k != 'page'])

		return ctx


class VoterDetailView(DetailView):
	"""View to display details of a single voter"""
	model = Voter
	template_name = 'voter_analytics/voter_detail.html'
	context_object_name = 'voter'


class GraphsListView(ListView):
	"""View to display graphs of voter analytics data"""
	model = Voter
	template_name = 'voter_analytics/graphs.html'
	context_object_name = 'voters'

	def get_queryset(self):
		"""Apply the same filtering logic as VoterListView"""
		qs = Voter.objects.all()

		# apply simple filters that can be done in the DB
		party = self.request.GET.get('party')
		if party:
			qs = qs.filter(party=party)

		score = self.request.GET.get('voter_score')
		if score and score.isdigit():
			qs = qs.filter(voter_score=int(score))

		# election flags: if present and value is 'on' filter v==1
		elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
		for e in elections:
			if self.request.GET.get(e) == 'on':
				qs = qs.filter(**{e: 1})

		# date-of-birth year min/max need parsing of text field; do in Python
		min_year = self.request.GET.get('min_dob')
		max_year = self.request.GET.get('max_dob')

		if min_year or max_year:
			min_y = int(min_year) if (min_year and min_year.isdigit()) else None
			max_y = int(max_year) if (max_year and max_year.isdigit()) else None

			# convert queryset to list and filter by extracted year
			filtered = []
			for v in qs:
				y = _extract_year(v.date_of_birth)
				if y is None:
					continue
				if min_y and y < min_y:
					continue
				if max_y and y > max_y:
					continue
				filtered.append(v)
			return filtered

		return qs

	def get_context_data(self, **kwargs):
		"""Create graphs and add them to context"""
		context = super().get_context_data(**kwargs)
		voters = self.get_queryset()

		# Graph 1: Histogram of voters by year of birth
		birth_years = []
		for voter in voters:
			year = _extract_year(voter.date_of_birth)
			if year:
				birth_years.append(year)
		
		year_counts = Counter(birth_years)
		years = sorted(year_counts.keys())
		counts = [year_counts[year] for year in years]
		
		# bar chart of voters by year of birth
		fig_birth = go.Bar(x=years, y=counts)
		graph_div_birth = plotly.offline.plot({
			"data": [fig_birth],
			"layout_title_text": "Distribution of Voters by Year of Birth"
		}, auto_open=False, output_type="div")
		context['graph_div_birth'] = graph_div_birth

		# Graph 2: Pie chart of voters by party affiliation
		parties = [voter.party or 'Unknown' for voter in voters]
		party_counts = Counter(parties)
		
		fig_party = go.Pie(labels=list(party_counts.keys()), values=list(party_counts.values()))
		graph_div_party = plotly.offline.plot({
			"data": [fig_party],
			"layout_title_text": "Distribution of Voters by Party Affiliation"
		}, auto_open=False, output_type="div")
		context['graph_div_party'] = graph_div_party

		# Graph 3: Histogram of election participation
		election_names = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
		election_labels = ['2020 State', '2021 Town', '2021 Primary', '2022 General', '2023 Town']
		election_counts = []
		
		for election in election_names:
			count = sum(1 for voter in voters if getattr(voter, election) == 1)
			election_counts.append(count)
		
		fig_elections = go.Bar(x=election_labels, y=election_counts)
		graph_div_elections = plotly.offline.plot({
			"data": [fig_elections],
			"layout_title_text": "Voter Participation in Recent Elections"
		}, auto_open=False, output_type="div")
		context['graph_div_elections'] = graph_div_elections

		# Add filter choices (reuse from VoterListView)
		context['parties'] = Voter.objects.values_list('party', flat=True).distinct().order_by('party')
		years = set()
		for dob in Voter.objects.values_list('date_of_birth', flat=True):
			y = _extract_year(dob)
			if y:
				years.add(y)
		context['years'] = sorted(years)
		context['scores'] = Voter.objects.values_list('voter_score', flat=True).distinct().order_by('-voter_score')

		return context

