from django.db import models

# Create your models here.

# Model -- Client Request Model


class ClientRequestModel(models.Model):
    """
        The client request model will hold persistent data about a 
        request a client has made in the shop.
        Therefore each client has its own record of what he has ever order
        in the shop.
        The data we're keeping are:

            - nom_du_client     : the last of the client
            ---------------------------: Those two above are held in ClientModel...
            - produit_demander  : the product he has requested 
            - found             : if the shop has satisfied the client or no.
    """

    client = models.ForeignKey(
        to='clients.ClientModel', on_delete=models.CASCADE)
    produit_demander = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    found = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    wished_price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{} {} {}'.format(self.client.fname, self.client.lname, self.found)
