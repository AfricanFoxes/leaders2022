from django.db import models
from djgeojson.fields import PointField, MultiPolygonField


class PObject(models.Model):
	index = models.IntegerField()
	type = models.CharField(max_length=20, verbose_name="type")
	name = models.CharField(max_length=100)
	geometry_name = models.CharField(max_length=100, null=True, blank=True)
	lon = models.FloatField()
	lat = models.FloatField()
	distance_to_center = models.FloatField()
	count_nearest_postamats = models.IntegerField()
	count_nearest_pvz = models.IntegerField()
	food_delivery = models.IntegerField()
	digitalization = models.FloatField()
	covering_postamats = models.IntegerField()
	normalize_name = models.CharField(max_length=20)
	okato = models.BigIntegerField()
	count_nearest_metro = models.IntegerField()
	level_working_region = models.IntegerField()
	level_sleeping_region = models.IntegerField()
	count_house_flat = models.IntegerField()
	population_house_flat = models.IntegerField()
	population_house_square = models.IntegerField()
	population_house_living_square = models.IntegerField()
	count_house_flat_400 = models.IntegerField()
	population_house_flat_400 = models.IntegerField()
	population_house_square_400 = models.IntegerField()
	population_house_living_square_400 = models.IntegerField()
	count_house_flat_200 = models.IntegerField()
	population_house_flat_200 = models.IntegerField()
	population_house_square_200 = models.IntegerField()
	population_house_living_square_200 = models.IntegerField()
	geometry = PointField()

	def __str__(self):
		return self.name


class Region(models.Model):
	name = models.CharField(max_length=100)
	p_type = models.CharField(max_length=20)
	index = models.IntegerField()
	geometry = MultiPolygonField()

	def __str__(self):
		return self.name
