# File: voter_analytics/models.py
# Author: Saksham Goel (sakshamg@bu.edu), 10/27/2025
# Description: Models for the voter_analytics application, including Voter model.

from django.db import models

# Create your models here.


class Voter(models.Model):
	'''Represent a registered voter in Newton, MA. Columns in the CSV:
	Voter ID Number,Last Name,First Name,Residential Address - Street Number,
	Residential Address - Street Name,Residential Address - Apartment Number,
	Residential Address - Zip Code,Date of Birth,Date of Registration,
	Party Affiliation,Precinct Number,v20state,v21town,v21primary,v22general,v23town,voter_score
	'''
	# identification
	last_name = models.TextField()
	first_name = models.TextField()

	# address pieces
	street_number = models.CharField(max_length=20, blank=True, null=True)
	street_name = models.TextField(blank=True, null=True)
	apt_number = models.CharField(max_length=20, blank=True, null=True)
	zip_code = models.CharField(max_length=12, blank=True, null=True)

	# dates
	date_of_birth = models.TextField(blank=True, null=True)
	date_of_registration = models.TextField(blank=True, null=True)

	# political info
	party = models.CharField(max_length=2, blank=True, null=True)
	precinct = models.CharField(max_length=10, blank=True, null=True)

	# participation flags for recent elections
	v20state = models.IntegerField(default=0)
	v21town = models.IntegerField(default=0)
	v21primary = models.IntegerField(default=0)
	v22general = models.IntegerField(default=0)
	v23town = models.IntegerField(default=0)

	voter_score = models.IntegerField(default=0)

	def __str__(self):
		return f"{self.first_name} {self.last_name} ({self.party or 'NA'}) - {self.zip_code or 'NA'}"


def load_data():
	"""Load voters from the given CSV file into the database.

	This follows the simple loader style used in `marathon_analytics.models`:
	- skip the header line
	- split on commas
	- be tolerant of missing fields
	"""
	filename = '/Users/sakshamgoel/Desktop/newton_voters.csv'
	print(f"Loading voters from: {filename}")

	try:
		f = open(filename, 'r')
	except Exception as e:
		print(f"Unable to open file: {e}")
		return

	header = f.readline()  # skip header

	created = 0
	for line in f:
		fields = [s.strip() for s in line.strip().split(',')]

		# guard against short/malformed lines
		if len(fields) < 16:
			print(f"Skipping malformed line (fields={len(fields)}): {line}")
			continue

		# create a Voter object and save it to the database
		try:
			voter = Voter(
				last_name=fields[1],
				first_name=fields[2],
				street_number=fields[3] or None,
				street_name=fields[4] or None,
				apt_number=fields[5] or None,
				zip_code=fields[6] or None,
				date_of_birth=fields[7] or None,
				date_of_registration=fields[8] or None,
				party=fields[9] or None,
				precinct=fields[10] or None,
				v20state=1 if fields[11].upper() == 'TRUE' else 0,
				v21town=1 if fields[12].upper() == 'TRUE' else 0,
				v21primary=1 if fields[13].upper() == 'TRUE' else 0,
				v22general=1 if fields[14].upper() == 'TRUE' else 0,
				v23town=1 if fields[15].upper() == 'TRUE' else 0,
				voter_score=int(fields[16]) if len(fields) > 16 and fields[16].isdigit() else 0,
			)
			voter.save()
			created += 1
			if created % 5000 == 0:
				print(f"Created {created} voters so far...")
		except Exception as e:
			print("Failed to create Voter for line:")
			print(line)
			print(e)

	f.close()
	total = Voter.objects.count()
	print(f"Done. Created ~{created} new records. Total voters in DB: {total}")
