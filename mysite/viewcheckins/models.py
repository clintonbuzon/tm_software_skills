from django.db import models

# Create your models here.
class Dailycheckins(models.Model):
    id = models.IntegerField(primary_key=True, blank=True, null=False)  # AutoField?
    user = models.TextField(blank=True, null=True)
    original_timestamp = models.TextField(blank=True, null=True)
    hours = models.TextField(blank=True, null=True)
    project = models.TextField(blank=True, null=True)
    cleaned_timestamp = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'dailycheckins'