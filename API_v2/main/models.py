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
	normalize_name = models.CharField(max_length=100)
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
	NAME = models.CharField(max_length=100)
	OSM_ID = models.BigIntegerField()
	oktmo = models.CharField(max_length=20, null=True)
	okato = models.BigIntegerField()
	normalize_name = models.CharField(max_length=100)
	region_average_age = models.FloatField()
	region_population = models.IntegerField()
	average_salary = models.IntegerField()
	average_employees = models.IntegerField()
	prc_employees_small_businesses = models.FloatField()
	count_small_enterprises = models.IntegerField()
	investments = models.IntegerField()
	price_metr_housing = models.IntegerField()
	cost_apartment = models.IntegerField()
	rating_ecology = models.IntegerField()
	entertainment_infrastructure = models.IntegerField()
	house_infrastructure_rating = models.IntegerField()
	prc_xenophobic = models.FloatField()
	area_per_human_region = models.FloatField()
	population_density_region = models.FloatField()
	population_region = models.IntegerField()
	prc_people_higher_education = models.FloatField()
	death_rate = models.FloatField()
	total_fertility_rate = models.FloatField()
	prc_children = models.FloatField()
	budget_expenditures = models.IntegerField()
	budget_revenues = models.IntegerField()
	geometry = MultiPolygonField()

	def __str__(self):
		return self.NAME
