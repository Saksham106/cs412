from django.db import models

# Create your models here.


class Voter(models.Model):
	'''Represent a registered voter in Newton, MA. Columns in the CSV:
	Voter ID Number,Last Name,First Name,Residential Address - Street Number,
	Residential Address - Street Name,Residential Address - Apartment Number,
	Residential Address - Zip Code,Date of Birth,Date of Registration,
	Party Affiliation,Precinct Number,v20state,v21town,v21primary,v22general,v23town,voter_score
	'''

	last_name = models.TextField()
	first_name = models.TextField()

	# address pieces
	street_number = models.CharField(max_length=20, blank=True, null=True)
	street_name = models.TextField(blank=True, null=True)
	apt_number = models.CharField(max_length=20, blank=True, null=True)
	zip_code = models.CharField(max_length=12, blank=True, null=True)

	date_of_birth = models.TextField(blank=True, null=True)
	date_of_registration = models.TextField(blank=True, null=True)

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
				v20state=int(fields[11]) if fields[11].isdigit() else 0,
				v21town=int(fields[12]) if fields[12].isdigit() else 0,
				v21primary=int(fields[13]) if fields[13].isdigit() else 0,
				v22general=int(fields[14]) if fields[14].isdigit() else 0,
				v23town=int(fields[15]) if fields[15].isdigit() else 0,
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
