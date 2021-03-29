from django.db import models


# Create your models here.
class SeoResult(models.Model):
	domain = models.CharField(max_length=1000, null=True)
	title = models.CharField(max_length=1000, null=True)
	description = models.TextField(null=True)
	url = models.URLField(null=True)
	parse_number = models.IntegerField(default=1)
	keywords = models.TextField()
	engine = models.TextField()
	location = models.TextField()
