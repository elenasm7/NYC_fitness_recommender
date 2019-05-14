from django.db import models

# Create your models here.

class Company(models.Model):
	index = models.IntegerField(primary_key=True)
	rev_comp_id = models.TextField()
	categories = models.CharField(max_length=100)
	review_count = models.IntegerField()
	rating = models.FloatField()
	rev_company_name = models.CharField(max_length=100)
	