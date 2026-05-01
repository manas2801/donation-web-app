from django.db import models
from django.contrib.auth.models import User

class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    donor_name = models.CharField(max_length=100)
    amount = models.IntegerField()
    status = models.CharField(max_length=20, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.donor_name