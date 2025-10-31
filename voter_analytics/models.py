from django.db import models

# Create your models here.

class Voter(models.Model):
    """Store/Represents a registered voter. 
    Will use all attributes from the voter file."""

    #identification 
    last_name = models.TextField()
    first_name = models.TextField()

    # residency
    street_number = models.IntegerField()
    street_name = models.TextField()
    apartment_number = models.TextField(blank=True)
    zip_code = models.CharField(max_length=10)

    #birth info
    dob = models.DateField()

    # registration info
    registration_date = models.DateField()
    party_affiliation = models.CharField(max_length=2)
    precinct = models.IntegerField()

    # recent election participation
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)

    # sum of recent participation
    # indicated how many of the past 5 elections the voter participated in
    voter_score = models.IntegerField()

    def __str__(self):
        """String representation of the Voter instance."""
        return f"{self.last_name}, {self.first_name} ({self.voter_ID})"

def load_data():
    """ function to load data into the Voter model from a CSV file. """

    
    filename = '/Users/angelierose/desktop/newton_voters.csv'
    f = open(filename, 'r') # open file for reading

    f.readline() # skip header line 
    
    for line in f: #read the entire file, one line at a time
        try: 
            fields = line.strip().split(',')
            
            result = Voter(
                last_name = fields[1],
                first_name = fields[2],
                street_number = int(fields[3]),
                street_name = fields[4],
                apartment_number = fields[5],
                zip_code = fields[6],
                dob = fields[7],
                registration_date = fields[8],
                party_affiliation = fields[9],
                precinct = int(fields[10]),
                v20state = fields[11] == 'TRUE',
                v21town = fields[12] == 'TRUE',
                v21primary = fields[13] == 'TRUE',
                v22general = fields[14] == 'TRUE',
                v23town = fields[15] == 'TRUE',
                voter_score = int(fields[16])
            )
            result.save()  # save the instance to the database
            # print(f"Created Voter: {result}")
        except Exception as e:
            print(f"ERROR processing line: {line}")

        print(f"Finished and Created {len(Voter.objects.all())} voters")

