from django.db import models

# Create your models here.

from django.db import models

class User(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15, unique=True)
    mail = models.EmailField(unique=True)
    id_card = models.CharField(max_length=50, unique=True)
    city = models.CharField(max_length=50)
    number_of_tickets = models.PositiveIntegerField()

    # Tickets (Optional, up to 6)
    ticket1 = models.CharField(max_length=50, blank=True, null=True)
    ticket2 = models.CharField(max_length=50, blank=True, null=True)
    ticket3 = models.CharField(max_length=50, blank=True, null=True)
    ticket4 = models.CharField(max_length=50, blank=True, null=True)
    ticket5 = models.CharField(max_length=50, blank=True, null=True)
    ticket6 = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.mail})"

    def get_tickets(self):
        """Return all non-empty tickets as a list."""
        return [ticket for ticket in [
            self.ticket1, self.ticket2, self.ticket3,
            self.ticket4, self.ticket5, self.ticket6
        ] if ticket]
