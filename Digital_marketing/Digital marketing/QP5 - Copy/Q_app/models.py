from django.db import models
import os
from django.db.models.deletion import CASCADE
from django.db.models.base import Model
# Create your models here.

class logindetails(models.Model):
    username=models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    role=models.CharField(max_length=20)
    mail=models.EmailField(max_length=30)

def upload_path(instance, filename):
    # change the filename here is required
    return os.path.join("uploads", filename)


class clientdetails(models.Model):
    clientname=models.CharField(max_length=50)
    
    userid=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    date=models.CharField(max_length=50)
    image=models.ImageField(upload_to=upload_path)


class requirements(models.Model):
    deptid  = models.ForeignKey(clientdetails,on_delete=CASCADE)
    name = models.CharField(max_length=100)
    
    campaign_name = models.CharField(max_length=100)
    start_date = models.CharField(max_length=100)
    end_date = models.CharField(max_length=100)
    planned_impressions = models.CharField(max_length=100)
    planned_cpm = models.CharField(max_length=100)
    planned_cpc = models.CharField(max_length=100)
    planned_cost = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class person(models.Model):
    name = models.CharField(max_length=100)

class user_report(models.Model):
    clientname = models.CharField(max_length=100)
    campaign_name = models.CharField(max_length=100)
    date=models.CharField(max_length=10)
    no_of_impressions=models.IntegerField()
    no_of_clicks=models.IntegerField()
    cost_per_impressions=models.IntegerField()
    cost_per_click=models.IntegerField()
    total_cost_per_impressions=models.IntegerField()
    total_cost_per_click=models.IntegerField()
    cost_per_day=models.IntegerField()
