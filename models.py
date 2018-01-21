from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# from geofence.form import ChildForm

class Company(models.Model):
    name =  models.CharField(max_length = 200) 
    def __unicode__(self):
        return unicode(self.name)



class Driver(models.Model):
    driver = models.CharField(max_length = 200) # DRIVER_NAME
    company =  models.CharField(max_length = 200) # OWNER_NAME
    cpn = models.ForeignKey(Company, default = '')
    driver_id = models.CharField(max_length = 200, default = '') # DRIVER_ID
    def __unicode__(self):
        return unicode(self.driver)

GEO_CATEGORY = ( ('normal', 'normal'), ('parent', 'parent'), ('child', 'child') )

class Geofence(models.Model):
    geofence = models.CharField(max_length = 200, default = '', unique=True)  
    description = models.CharField(max_length = 200, default = '', null=True)
    pos_time = models.CharField(max_length = 200, default = '')
    enter_lat = models.CharField(max_length = 200, default = '')
    enter_long = models.CharField(max_length = 200, default = '')
    exit_lat = models.CharField(max_length = 200, default = '', null=True)
    exit_long = models.CharField(max_length = 200, default = '', null=True)
    pos_heading = models.CharField(max_length = 200, default = '')
    pos_address = models.CharField(max_length = 200, default = '')  
    geo_category = models.CharField(max_length = 200,choices = GEO_CATEGORY, default = 'normal')


    def __unicode__(self):
        return unicode(self.geofence)

class Child(models.Model):
    child_geofence = models.CharField(max_length = 200, default = '', unique=True)  
    description = models.CharField(max_length = 200, default = '', null=True)
    pos_time = models.CharField(max_length = 200, default = '')
    enter_lat = models.CharField(max_length = 200, default = '')
    enter_long = models.CharField(max_length = 200, default = '')
    exit_lat = models.CharField(max_length = 200, default = '', null=True)
    exit_long = models.CharField(max_length = 200, default = '', null = True)
    pos_heading = models.CharField(max_length = 200, default = '')
    pos_address = models.CharField(max_length = 200, default = '')  
    geo_category = models.CharField(max_length = 200,choices = GEO_CATEGORY, default = 'normal')
    

    def __unicode__(self):
        return unicode(self.child_geofence)

class Vehicle(models.Model):
    company =  models.CharField(max_length = 200)
    
    driver = models.ForeignKey(Driver, null=True, blank=True, on_delete = models.CASCADE)
    plate = models.CharField(max_length = 200, default = '')
    
    geofence = models.ForeignKey(Geofence, null= True, blank=True,  on_delete = models.CASCADE)
    child_geofence = models.ForeignKey(Child, null= True, blank=True, on_delete = models.CASCADE)
    
    geo_time =  models.CharField(max_length = 200, default = '', null= True, blank=True)
    event_duration = models.IntegerField(default = 0, null= True, blank=True)

    geotype = models.CharField(max_length = 200, default = '', null= True, blank=True)
    child_geotype = models.CharField(max_length = 200, default = '', null= True, blank=True)

    response = models.CharField(max_length = 200, null= True, blank=True)
    child_response = models.CharField(max_length = 200,  null= True, blank=True)

    cpn = models.ForeignKey(Company, default = '', blank=True, null = True)

    def __unicode__(self):
        return unicode(self.plate)

class History(models.Model):
    company =  models.CharField(max_length = 200)
    
    driver = models.ForeignKey(Driver, null=True, blank=True, on_delete = models.CASCADE)
    plate = models.CharField(max_length = 200, default = '')
    
    geofence = models.ForeignKey(Geofence, null= True, blank=True,  on_delete = models.CASCADE)
    child_geofence = models.ForeignKey(Child, null= True, blank=True, on_delete = models.CASCADE)
    
    geo_time =  models.CharField(max_length = 200, default = '', null= True, blank=True)
    event_duration = models.IntegerField(default = 0, null= True, blank=True)

    geotype = models.CharField(max_length = 200, default = '', null= True, blank=True)
    child_geotype = models.CharField(max_length = 200, default = '', null= True, blank=True)

    response = models.CharField(max_length = 200, null= True, blank=True)
    child_response = models.CharField(max_length = 200,  null= True, blank=True)

    cpn = models.ForeignKey(Company, default = '', blank=True, null = True)
    def __unicode__(self):
        return unicode(self.plate)

    @classmethod
    def create(cls, plate, driver, company, geofence, geo_time, event_duration, geotype):
        vehicle = cls(plate=plate, driver=driver, company=company, geofence=geofence, geo_time=geo_time,
            event_duration=event_duration, geotype=geotype)
        return vehicle

@receiver(post_save, sender=Vehicle)
def create_history(sender, instance, **kwargs):
    o = History.create(instance.plate, instance.driver, instance.company, instance.geofence, instance.geo_time,
        instance.event_duration, instance.geotype)
    o.save()



    # @property
    # def create_child_list(self, geofence):
    #     parent_child_dict = {'A': ['a', 'b', 'c', 'd'], 'B': ['e', 'f', 'g', 'h']}
    #     for key in parent_child_dict:
    #         if geofence.geofence == key:
    #             return parent_child_dict[key]

    # CHILD_LIST = (('DEFAULT', ''), ('EMPTY', ''))

    # child_geofence = models.CharField(max_length = 200, choices= CHILD_LIST, default = '', null = True, blank= True)



    



    # owner_name = models.CharField(max_length = 200, default = '') # Driver.company
    # driver_name = models.CharField(max_length = 200, default = '') # Driver.driver
    # driver_id = models.CharField(max_length = 200, default = '') # Driver.driver_id





