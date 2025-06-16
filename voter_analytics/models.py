from django.db import models
from datetime import datetime

# Create your models here.
from django.db import models

# Create your models here.
class Voter(models.Model):
    '''
    Store/represent the data from one voter in Newton.
    '''
    # identification
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    address_street_number = models.TextField(blank=True)
    address_street_name = models.TextField(blank=True)
    address_apartment_number = models.TextField(blank=True)
    address_zip_code = models.IntegerField(blank=True)
    date_of_birth = models.DateField(blank=True)
    date_of_registration = models.DateField(blank=True)

    # political participation
    party_affiliation = models.CharField(max_length=2, blank=True)
    precinct_number = models.TextField(blank=True)
    v20state = models.BooleanField(null=True)
    v21town = models.BooleanField(null=True)
    v21primary = models.BooleanField(null=True)
    v22general = models.BooleanField(null=True)
    v23town = models.BooleanField(null=True)
    voter_score = models.IntegerField(blank=True)

    def __str__(self):
        '''Return the full name of a Voter'''
        return f'{self.first_name} {self.last_name}'
    
    def address(self):
        """Return a readable string representation of the address of a Voter"""
        return f'{self.address_street_number} {self.address_street_name}, Apartment {self.address_apartment_number}, Newton, MA'
         
def text_to_datefield(text):
    """Parses the """

def load_data():
    '''Function to load data records from CSV file into Django model instances.'''

    filename = '/Users/jeffreyzhou/Desktop/newton_voters.csv'
    f = open(filename)
    f.readline() # discard headers

    for line in f:
        fields = line.replace('\n', '').split(',')

        try:
            voter = Voter(first_name=fields[1],
                          last_name=fields[2],
                          address_street_number=fields[3],
                          address_street_name=fields[4],
                          address_apartment_number=fields[5],
                          address_zip_code=int(fields[6]),
                          date_of_birth=datetime.strptime(fields[7], "%Y-%m-%d").date(),
                          date_of_registration=datetime.strptime(fields[8], "%Y-%m-%d").date(),
                          party_affiliation=fields[9],
                          precinct_number=fields[10],
                          v20state=fields[11].upper() == 'TRUE',
                          v21town=fields[12].upper() == 'TRUE',
                          v21primary=fields[13].upper() == 'TRUE',
                          v22general=fields[14].upper() == 'TRUE',
                          v23town=fields[15].upper() == 'TRUE',
                          voter_score=int(fields[16]),
                        )
            voter.save()
            print(f'Created voter {voter}.')
        except:
            print(f"Skipped: {fields}")