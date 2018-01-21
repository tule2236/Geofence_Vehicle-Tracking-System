from django.shortcuts import render, get_object_or_404
from geofence.models import Driver, Geofence, Vehicle, History,Child
import requests
from bs4 import BeautifulSoup
import urllib
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from datetime import datetime
from django.utils import timezone
from dateutil import tz
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from geofence.form import DriverForm, GeofenceForm, ChildForm
from django.utils.decorators import method_decorator

#(name='geofence')
# decorators = [never_cache]
@method_decorator(login_required, name='geofence')
class VehicleList(ListView):
    template_name = 'geofence/geo_display.html'
    queryset = Vehicle.objects.all()

    # @method_decorator
    def geofence(self, request, *args, **kwargs):
        if request.method == 'GET':
           
            EVENT_TIME=request.GET['EVENT_TIME']
            EVENT_DURATION=request.GET['EVENT_DURATION']
            # USER_USERNAME=request.GET['USER_USERNAME']
            USER_NAME=request.GET['USER_NAME'] # key to match with Driver table
            USER_DESCRIPTION=request.GET['USER_DESCRIPTION']
            POS_TIME=request.GET['POS_TIME']
            POS_LATITUDE=request.GET['POS_LATITUDE']
            POS_LONGITUDE=request.GET['POS_LONGITUDE']
            POS_HEADING=request.GET['POS_HEADING']
            POS_ADDRESS=request.GET['POS_ADDRESS']
            GEOFENCE_NAME=request.GET['GEOFENCE_NAME']
            GEOTYPE=request.GET['GEOTYPE']

        matched_vehicle = Vehicle.objects.filter(plate = USER_NAME) # get corresponding Vehicle objects
        matched_driver = matched_vehicle[0].driver

        OWNER_NAME = matched_driver.company
        DRIVER_NAME = matched_driver.driver
        DRIVER_ID = matched_driver.driver_id

        from_zone, to_zone = tz.gettz('UTC'), tz.gettz('Asia/Singapore')
        date = datetime.strptime(EVENT_TIME, '%Y-%m-%dT%H:%M:%S').replace(tzinfo = from_zone).astimezone(to_zone)
        dtTime = datetime.strftime(date, '%d/%m/%Y %H:%M')
    # http://127.0.0.1:8000/geofence/?EVENT_TIME=%20A&EVENT_DURATION=20&USER_NAME=%201234&USER_DESCRIPTION=%20A&POS_TIME=%20A&POS_LATITUDE=%20123&POS_LONGITUDE=%20435&POS_HEADING=%20A&POS_ADDRESS=%20SKYFY&GEOFENCE_NAME=%20A&GEOTYPE=%201
            # sentstring="http://118.201.213.62/apsg/apsg.php?proc=vehtrackupdate&VEHNO=%22USER_NAME%22&VEHGRP=%22APSG%22&VEHSUBGRP=%22OWNER_NAME%22&GEONAME=%22GEOFENCE%22&GEODESC=%22APSG%22&GEOTYPE=%22GEOTYPE%22&GEOTIME=%22dtTime%22&DURATION=EVENT_DURATION&DRVNAME=%22DRIVER_NAME%20XINGJUE%22&DRIVERID=%22DRIVER_ID%22&VTSVENDOR=%22SF%22&VLNG=%22POS_LONGITUDE%22&VLAT=%22POS_LATITUDE%22"
        geofence = Geofence(description=USER_DESCRIPTION, pos_time=POS_TIME, pos_lat=POS_LATITUDE, pos_long=POS_LONGITUDE,pos_heading=POS_HEADING, pos_address=POS_ADDRESS, geofence=GEOFENCE_NAME)
        geofence.save()
        geofence= Geofence.objects.get(geofence=GEOFENCE_NAME)

        sentstring = "http://13.229.83.167/Test.php?VEHNO=%22"+USER_NAME+"%22&VEHGRP=%22APSG%22&VEHSUBGRP=%22"+OWNER_NAME+"%22&GEONAME=%22"+GEOFENCE_NAME+"%22&GEODESC=%22APSG%22&GEOTYPE=%22"+GEOTYPE+"%22&GEOTIME=%223"+dtTime+"%22&DURATION="+str(EVENT_DURATION)+"&DRVNAME=%22"+DRIVER_NAME+"%22&DRIVERID=%22"+DRIVER_ID+"%22&VTSVENDOR=%22SF%22&VLNG=%22"+POS_LONGITUDE+"%22&VLAT=%22"+POS_LATITUDE+"%22"
        response = requests.get(sentstring)
        r = response.text.encode('latin-1')

        matched_vehicle.update(event_duration=EVENT_DURATION, geo_time=dtTime, geotype=GEOTYPE, response=r)

        matched_vehicle.update(geofence = geofence)
        matched_vehicle[0].save()

        o = History(plate=plate, driver=matched_driver, company=company, geofence=geofence, geo_time=geo_time,
            event_duration=event_duration, geotype=geotype)
        o.save()
        # return render(request, 'geofence/geo_display.html')

        # return super(VehicleList, self).geofence(request, *args, **kwargs)

def update_driver_db(request, pk):
    vehicle_instance = get_object_or_404(Vehicle, pk = pk)
    # the_company = vehicle_instance.cpn
    
    if request.method == 'POST':
        form = DriverForm(the_company, request.POST)
        # Driver[company] == Vehicle.driver.driver
        # form.fields["company"].queryset = Driver.objects.filter(company = the_company)
        if form.is_valid():
            Vehicle.objects.filter(pk = vehicle_instance.pk).update(driver = form.cleaned_data['driver'])
            # form.save()
            return HttpResponseRedirect('/geofence/geolist')
    else:
    #   proposed_driver = Vehicle.objects.filter(company=the_company)
      # form = DriverForm(company=the_company)
        form = DriverForm
    return render(request, 'geofence/driver_form.html', {'form': form, 'vehicle_instance': vehicle_instance})

def geofence_assignment(request, pk):
    vehicle_instance = get_object_or_404(Vehicle, pk = pk)
    
    if request.method == 'POST':
        form = GeofenceForm(request.POST)
        if form.is_valid():
            
            EVENT_TIME = timezone.now()
            from_zone, to_zone = tz.gettz('UTC'), tz.gettz('Asia/Singapore')
            date = EVENT_TIME.replace(tzinfo = from_zone).astimezone(to_zone)
            dtTime = datetime.strftime(date, '%d/%m/%Y %H:%M')

            EVENT_DURATION= vehicle_instance.event_duration
            USER_NAME= vehicle_instance.plate
            ENTER_LATITUDE= form.cleaned_data['geofence'].enter_lat
            ENTER_LONGITUDE= form.cleaned_data['geofence'].enter_long
            EXIT_LATITUDE= form.cleaned_data['geofence'].exit_lat
            EXIT_LONGITUDE= form.cleaned_data['geofence'].exit_long
            GEOFENCE_NAME= form.cleaned_data['geofence'].geofence
            GEOTYPE=  form.cleaned_data['geotype']
            OWNER_NAME = vehicle_instance.driver.company
            DRIVER_NAME = vehicle_instance.driver.driver
            DRIVER_ID = vehicle_instance.driver.driver_id
           
            if GEOTYPE == '1':
                sentstring = "http://13.229.83.167/Test.php?VEHNO=%22"+USER_NAME+"%22&VEHGRP=%22APSG%22&VEHSUBGRP=%22"+OWNER_NAME+"%22&GEONAME=%22"+GEOFENCE_NAME+"%22&GEODESC=%22APSG%22&GEOTYPE=%22"+GEOTYPE+"%22&GEOTIME=%223"+dtTime+"%22&DURATION="+str(EVENT_DURATION)+"&DRVNAME=%22"+DRIVER_NAME+"%22&DRIVERID=%22"+DRIVER_ID+"%22&VTSVENDOR=%22SF%22&VLNG=%22"+ENTER_LONGITUDE+"%22&VLAT=%22"+ENTER_LATITUDE+"%22"
                response = requests.get(sentstring)
                r = response.text.encode('latin-1')
                Vehicle.objects.filter(pk = vehicle_instance.pk).update(geofence = form.cleaned_data['geofence'], 
                geotype = form.cleaned_data['geotype'], response=r)
                
            elif GEOTYPE == '2':
                sentstring = "http://13.229.83.167/Test.php?VEHNO=%22"+USER_NAME+"%22&VEHGRP=%22APSG%22&VEHSUBGRP=%22"+OWNER_NAME+"%22&GEONAME=%22"+GEOFENCE_NAME+"%22&GEODESC=%22APSG%22&GEOTYPE=%22"+GEOTYPE+"%22&GEOTIME=%223"+dtTime+"%22&DURATION="+str(EVENT_DURATION)+"&DRVNAME=%22"+DRIVER_NAME+"%22&DRIVERID=%22"+DRIVER_ID+"%22&VTSVENDOR=%22SF%22&VLNG=%22"+EXIT_LONGITUDE+"%22&VLAT=%22"+EXIT_LATITUDE+"%22"
                response = requests.get(sentstring)
                Vehicle.objects.filter(pk = vehicle_instance.pk).update(geofence = None, 
                geotype = form.cleaned_data['geotype'], response='')
                
            
            o = History(plate=USER_NAME, driver=vehicle_instance.driver, company=OWNER_NAME, geofence=vehicle_instance.geofence,
            geo_time=dtTime, event_duration=EVENT_DURATION, geotype=GEOTYPE)
            o.save()
            return HttpResponseRedirect('/geofence/geolist')
    else:
        form = GeofenceForm() 
    return render(request, 'geofence/geofence_form.html', {'form': form, 'vehicle_instance': vehicle_instance})

def child_geofence_assignment(request, pk):
    vehicle_instance = get_object_or_404(Vehicle, pk = pk)
    
    if request.method == 'POST':
        form = ChildForm(request.POST)
        if form.is_valid():          
            EVENT_TIME = timezone.now()
            from_zone, to_zone = tz.gettz('UTC'), tz.gettz('Asia/Singapore')
            date = EVENT_TIME.replace(tzinfo = from_zone).astimezone(to_zone)
            dtTime = datetime.strftime(date, '%d/%m/%Y %H:%M')

            EVENT_DURATION= vehicle_instance.event_duration
            USER_NAME= vehicle_instance.plate
            ENTER_LATITUDE= form.cleaned_data['child'].enter_lat
            ENTER_LONGITUDE= form.cleaned_data['child'].enter_long
            EXIT_LATITUDE= form.cleaned_data['child'].exit_lat
            EXIT_LONGITUDE= form.cleaned_data['child'].exit_long

            GEOFENCE_NAME= form.cleaned_data['child'].child_geofence
            GEOTYPE=  vehicle_instance.geotype
            CHILD_GEOTYPE = form.cleaned_data['child_geotype'] 
            OWNER_NAME = vehicle_instance.driver.company
            DRIVER_NAME = vehicle_instance.driver.driver
            DRIVER_ID = vehicle_instance.driver.driver_id
            
            if CHILD_GEOTYPE == '1':
                sentstring = "http://13.229.83.167/Test.php?VEHNO=%22"+USER_NAME+"%22&VEHGRP=%22APSG%22&VEHSUBGRP=%22"+OWNER_NAME+"%22&GEONAME=%22"+GEOFENCE_NAME+"%22&GEODESC=%22APSG%22&GEOTYPE=%22"+GEOTYPE+"%22&GEOTIME=%223"+dtTime+"%22&DURATION="+str(EVENT_DURATION)+"&DRVNAME=%22"+DRIVER_NAME+"%22&DRIVERID=%22"+DRIVER_ID+"%22&VTSVENDOR=%22SF%22&VLNG=%22"+ENTER_LONGITUDE+"%22&VLAT=%22"+ENTER_LATITUDE+"%22"
                response = requests.get(sentstring)
            
                r = response.text.encode('latin-1')
                Vehicle.objects.filter(pk = vehicle_instance.pk).update(child_geofence = form.cleaned_data['child'], 
                child_geotype = form.cleaned_data['child_geotype'], child_response=r)
                
            elif CHILD_GEOTYPE == '2':
                sentstring = "http://13.229.83.167/Test.php?VEHNO=%22"+USER_NAME+"%22&VEHGRP=%22APSG%22&VEHSUBGRP=%22"+OWNER_NAME+"%22&GEONAME=%22"+GEOFENCE_NAME+"%22&GEODESC=%22APSG%22&GEOTYPE=%22"+GEOTYPE+"%22&GEOTIME=%223"+dtTime+"%22&DURATION="+str(EVENT_DURATION)+"&DRVNAME=%22"+DRIVER_NAME+"%22&DRIVERID=%22"+DRIVER_ID+"%22&VTSVENDOR=%22SF%22&VLNG=%22"+EXIT_LONGITUDE+"%22&VLAT=%22"+EXIT_LATITUDE+"%22"
                response = requests.get(sentstring)
            
                Vehicle.objects.filter(pk = vehicle_instance.pk).update(child_geofence = None, 
                child_geotype = form.cleaned_data['child_geotype'], child_response='')

                
            o = History(plate=USER_NAME, driver=vehicle_instance.driver, company=OWNER_NAME, geofence=vehicle_instance.geofence,
            geo_time=dtTime, event_duration=EVENT_DURATION, geotype=GEOTYPE, child_geofence=form.cleaned_data['child'],child_geotype=CHILD_GEOTYPE)
            o.save()
            return HttpResponseRedirect('/geofence/geolist')
    else:
        form = ChildForm() 
    return render(request, 'geofence/geofence_form.html', {'form': form, 'vehicle_instance': vehicle_instance})

class VehicleView(ListView):
    model = Vehicle
    context_object_name = 'vehicle_list'
    template_name = 'geofence/geo_display.html'
    queryset = Vehicle.objects.all()

    def get_context_data(self, **kwargs):
        context = super(VehicleView, self).get_context_data(**kwargs)

class VehicleSearchListView(ListView):
    model = Vehicle
    template_name = 'geofence/geo_display.html'

    def get_queryset(self):
        result = super(VehicleSearchListView, self).get_queryset()

        query = self.request.GET.get('q')
        
        if query:
            result = Vehicle.objects.all().filter(plate__icontains = query)
        return  result


def APSG_geofence(request):
    if request.method == 'GET':
       
        EVENT_TIME=request.GET['EVENT_TIME']
        EVENT_DURATION=request.GET['EVENT_DURATION']
        # USER_USERNAME=request.GET['USER_USERNAME']
        USER_NAME=request.GET['USER_NAME'] # key to match with Driver table
        USER_DESCRIPTION=request.GET['USER_DESCRIPTION']
        POS_TIME=request.GET['POS_TIME']
        POS_LATITUDE=request.GET['POS_LATITUDE']
        POS_LONGITUDE=request.GET['POS_LONGITUDE']
        POS_HEADING=request.GET['POS_HEADING']
        POS_ADDRESS=request.GET['POS_ADDRESS']
        GEOFENCE_NAME=request.GET['GEOFENCE_NAME']
        GEOTYPE=request.GET['GEOTYPE']
    
    matched_vehicle = Vehicle.objects.filter(plate = USER_NAME) # get corresponding Vehicle objects
    matched_driver = matched_vehicle[0].driver

    OWNER_NAME = matched_driver.company
    DRIVER_NAME = matched_driver.driver
    DRIVER_ID = matched_driver.driver_id

    from_zone, to_zone = tz.gettz('UTC'), tz.gettz('Asia/Singapore')
    date = datetime.strptime(EVENT_TIME, '%Y-%m-%dT%H:%M:%S').replace(tzinfo = from_zone).astimezone(to_zone)
    dtTime = datetime.strftime(date, '%d/%m/%Y %H:%M')
# http://127.0.0.1:8000/geofence/?EVENT_TIME=2017-05-08T09:09:09&EVENT_DURATION=20&USER_NAME=1234&USER_DESCRIPTION=%20A&POS_TIME=%20A&POS_LATITUDE=%20123&POS_LONGITUDE=%20435&POS_HEADING=%20A&POS_ADDRESS=%20SKYFY&GEOFENCE_NAME=A&GEOTYPE=2
    geo_list = Geofence.objects.filter(geofence=GEOFENCE_NAME)
    if len(geo_list) == 0:
        geofence = Geofence(description=USER_DESCRIPTION, pos_time=POS_TIME, enter_lat=POS_LATITUDE, enter_long=POS_LONGITUDE,
            pos_heading=POS_HEADING, pos_address=POS_ADDRESS, geofence=GEOFENCE_NAME)
        geofence.save()
    


    sentstring = "http://13.229.83.167/Test.php?VEHNO=%22"+USER_NAME+"%22&VEHGRP=%22APSG%22&VEHSUBGRP=%22"+OWNER_NAME+"%22&GEONAME=%22"+GEOFENCE_NAME+"%22&GEODESC=%22APSG%22&GEOTYPE=%22"+GEOTYPE+"%22&GEOTIME=%223"+dtTime+"%22&DURATION="+str(EVENT_DURATION)+"&DRVNAME=%22"+DRIVER_NAME+"%22&DRIVERID=%22"+DRIVER_ID+"%22&VTSVENDOR=%22SF%22&VLNG=%22"+POS_LONGITUDE+"%22&VLAT=%22"+POS_LATITUDE+"%22"
    response = requests.get(sentstring)
    response = response.text.encode('latin-1')

    if ((GEOTYPE == '1') and (matched_vehicle[0].geofence == None) and (matched_vehicle[0].child_geofence ==None)): # Enter the 1st gate              
        n='A'
        geo_list = Geofence.objects.filter(geofence=GEOFENCE_NAME)
        if len(geo_list) == 0:
            geofence = Geofence(description=USER_DESCRIPTION, pos_time=POS_TIME, enter_lat=POS_LATITUDE, enter_long=POS_LONGITUDE,
                pos_heading=POS_HEADING, pos_address=POS_ADDRESS, geofence=GEOFENCE_NAME)
            geofence.save()

        geofence= Geofence.objects.get(geofence=GEOFENCE_NAME)
        matched_vehicle.update(geotype=GEOTYPE, response=response,geofence= geofence)     
        o = History(plate=USER_NAME, driver=matched_driver, company=OWNER_NAME, geofence=geofence, geo_time=dtTime,
        event_duration=EVENT_DURATION, geotype=GEOTYPE)
        o.save()   

    elif GEOTYPE == '2' and matched_vehicle[0].geofence != None  and matched_vehicle[0].child_geofence ==None: # Exit the 1st gate
        n='B'
        geofence= Geofence.objects.get(geofence=GEOFENCE_NAME)
        matched_vehicle.update(geotype=GEOTYPE, response='', geofence=None)
        o = History(plate=USER_NAME, driver=matched_driver, company=OWNER_NAME, geofence=geofence, geo_time=dtTime,
        event_duration=EVENT_DURATION, geotype=GEOTYPE)
        o.save() 
    
    elif GEOTYPE == '1' and matched_vehicle[0].geofence != None and matched_vehicle[0].child_geofence == None: # Enter the child gate
        n='C'
        geo_list = Geofence.objects.filter(geofence=GEOFENCE_NAME)
        if len(geo_list) == 0:
            child_geofence = Child(description=USER_DESCRIPTION, pos_time=POS_TIME, enter_lat=POS_LATITUDE, enter_long=POS_LONGITUDE,
                pos_heading=POS_HEADING, pos_address=POS_ADDRESS, child_geofence=GEOFENCE_NAME)
            child_geofence.save()

            geofence = Geofence(description=USER_DESCRIPTION, pos_time=POS_TIME, enter_lat=POS_LATITUDE, enter_long=POS_LONGITUDE,
                pos_heading=POS_HEADING, pos_address=POS_ADDRESS, geofence=GEOFENCE_NAME)
            geofence.save()
            
        child_geofence= Child.objects.get(child_geofence=GEOFENCE_NAME)
        matched_vehicle.update(child_geotype=GEOTYPE, child_response=response, child_geofence=child_geofence)         
        geofence = Vehicle.objects.get(plate = USER_NAME).geofence
        geotype = Vehicle.objects.get(plate = USER_NAME).geotype
        o = History(plate=USER_NAME, driver=matched_driver, company=OWNER_NAME, geofence=geofence,geotype=geotype,child_geofence=child_geofence, 
            geo_time=dtTime, event_duration=EVENT_DURATION, child_geotype=GEOTYPE)
        o.save()      
    
    elif GEOTYPE == '2' and matched_vehicle[0].geofence != None and matched_vehicle[0].child_geofence != None: # Exit the child gate 
        n='D'
        child_geofence= Child.objects.get(child_geofence=GEOFENCE_NAME)
        geofence = Vehicle.objects.get(plate = USER_NAME).geofence
        geotype = Vehicle.objects.get(plate = USER_NAME).geotype
        matched_vehicle.update(child_geotype=GEOTYPE, child_response='', child_geofence=None)
        o = History(plate=USER_NAME, driver=matched_driver, company=OWNER_NAME, geofence=geofence,geotype=geotype,child_geofence=child_geofence, 
            geo_time=dtTime, event_duration=EVENT_DURATION, child_geotype=GEOTYPE)
        o.save() 
        
    return render(request, 'geofence/geo_display.html', {'data':n})



def TMSG_geofence(request):
    if request.method == 'GET':
       
        EVENT_TIME=request.GET['EVENT_TIME']
        EVENT_DURATION=request.GET['EVENT_DURATION']
        # USER_USERNAME=request.GET['USER_USERNAME']
        USER_NAME=request.GET['USER_NAME'] # key to match with Driver table
        USER_DESCRIPTION=request.GET['USER_DESCRIPTION']
        POS_TIME=request.GET['POS_TIME']
        POS_LATITUDE=request.GET['POS_LATITUDE']
        POS_LONGITUDE=request.GET['POS_LONGITUDE']
        POS_HEADING=request.GET['POS_HEADING']
        POS_ADDRESS=request.GET['POS_ADDRESS']
        GEOFENCE_NAME=request.GET['GEOFENCE_NAME']
        GEOTYPE=request.GET['GEOTYPE']
    
    matched_vehicle = Vehicle.objects.filter(plate = USER_NAME) # get corresponding Vehicle objects
    matched_driver = matched_vehicle[0].driver

    OWNER_NAME = matched_driver.company
    DRIVER_NAME = matched_driver.driver
    DRIVER_ID = matched_driver.driver_id

    from_zone, to_zone = tz.gettz('UTC'), tz.gettz('Asia/Singapore')
    date = datetime.strptime(EVENT_TIME, '%Y-%m-%dT%H:%M:%S').replace(tzinfo = from_zone).astimezone(to_zone)
    dtTime = datetime.strftime(date, '%d/%m/%Y %H:%M')
# http://127.0.0.1:8000/geofence/?EVENT_TIME=2017-05-08T09:09:09&EVENT_DURATION=20&USER_NAME=1234&USER_DESCRIPTION=%20A&POS_TIME=%20A&POS_LATITUDE=%20123&POS_LONGITUDE=%20435&POS_HEADING=%20A&POS_ADDRESS=%20SKYFY&GEOFENCE_NAME=A&GEOTYPE=2
    geo_list = Geofence.objects.filter(geofence=GEOFENCE_NAME)
    if len(geo_list) == 0:
        geofence = Geofence(description=USER_DESCRIPTION, pos_time=POS_TIME, enter_lat=POS_LATITUDE, enter_long=POS_LONGITUDE,
            pos_heading=POS_HEADING, pos_address=POS_ADDRESS, geofence=GEOFENCE_NAME)
        geofence.save()
    


    sentstring = "http://13.229.83.167/Test.php?VEHNO=%22"+USER_NAME+"%22&VEHGRP=%22APSG%22&VEHSUBGRP=%22"+OWNER_NAME+"%22&GEONAME=%22"+GEOFENCE_NAME+"%22&GEODESC=%22TMSG%22&GEOTYPE=%22"+GEOTYPE+"%22&GEOTIME=%223"+dtTime+"%22&DURATION="+str(EVENT_DURATION)+"&DRVNAME=%22"+DRIVER_NAME+"%22&DRIVERID=%22"+DRIVER_ID+"%22&VTSVENDOR=%22SF%22&VLNG=%22"+POS_LONGITUDE+"%22&VLAT=%22"+POS_LATITUDE+"%22"
    response = requests.get(sentstring)
    response = response.text.encode('latin-1')

    if ((GEOTYPE == '1') and (matched_vehicle[0].geofence == None) and (matched_vehicle[0].child_geofence ==None)): # Enter the 1st gate              
        n='A'
        geo_list = Geofence.objects.filter(geofence=GEOFENCE_NAME)
        if len(geo_list) == 0:
            geofence = Geofence(description=USER_DESCRIPTION, pos_time=POS_TIME, enter_lat=POS_LATITUDE, enter_long=POS_LONGITUDE,
                pos_heading=POS_HEADING, pos_address=POS_ADDRESS, geofence=GEOFENCE_NAME)
            geofence.save()

        geofence= Geofence.objects.get(geofence=GEOFENCE_NAME)
        matched_vehicle.update(geotype=GEOTYPE, response=response,geofence= geofence)     
        o = History(plate=USER_NAME, driver=matched_driver, company=OWNER_NAME, geofence=geofence, geo_time=dtTime,
        event_duration=EVENT_DURATION, geotype=GEOTYPE)
        o.save()   

    elif GEOTYPE == '2' and matched_vehicle[0].geofence != None  and matched_vehicle[0].child_geofence ==None: # Exit the 1st gate
        n='B'
        geofence= Geofence.objects.get(geofence=GEOFENCE_NAME)
        matched_vehicle.update(geotype=GEOTYPE, response='', geofence=None)
        o = History(plate=USER_NAME, driver=matched_driver, company=OWNER_NAME, geofence=geofence, geo_time=dtTime,
        event_duration=EVENT_DURATION, geotype=GEOTYPE)
        o.save() 
    
    elif GEOTYPE == '1' and matched_vehicle[0].geofence != None and matched_vehicle[0].child_geofence == None: # Enter the child gate
        n='C'
        geo_list = Geofence.objects.filter(geofence=GEOFENCE_NAME)
        if len(geo_list) == 0:
            child_geofence = Child(description=USER_DESCRIPTION, pos_time=POS_TIME, enter_lat=POS_LATITUDE, enter_long=POS_LONGITUDE,
                pos_heading=POS_HEADING, pos_address=POS_ADDRESS, child_geofence=GEOFENCE_NAME)
            child_geofence.save()

            geofence = Geofence(description=USER_DESCRIPTION, pos_time=POS_TIME, enter_lat=POS_LATITUDE, enter_long=POS_LONGITUDE,
                pos_heading=POS_HEADING, pos_address=POS_ADDRESS, geofence=GEOFENCE_NAME)
            geofence.save()
            
        child_geofence= Child.objects.get(child_geofence=GEOFENCE_NAME)
        matched_vehicle.update(child_geotype=GEOTYPE, child_response=response, child_geofence=child_geofence)         
        geofence = Vehicle.objects.get(plate = USER_NAME).geofence
        geotype = Vehicle.objects.get(plate = USER_NAME).geotype
        o = History(plate=USER_NAME, driver=matched_driver, company=OWNER_NAME, geofence=geofence,geotype=geotype,child_geofence=child_geofence, 
            geo_time=dtTime, event_duration=EVENT_DURATION, child_geotype=GEOTYPE)
        o.save()      
    
    elif GEOTYPE == '2' and matched_vehicle[0].geofence != None and matched_vehicle[0].child_geofence != None: # Exit the child gate 
        n='D'
        child_geofence= Child.objects.get(child_geofence=GEOFENCE_NAME)
        geofence = Vehicle.objects.get(plate = USER_NAME).geofence
        geotype = Vehicle.objects.get(plate = USER_NAME).geotype
        matched_vehicle.update(child_geotype=GEOTYPE, child_response='', child_geofence=None)
        o = History(plate=USER_NAME, driver=matched_driver, company=OWNER_NAME, geofence=geofence,geotype=geotype,child_geofence=child_geofence, 
            geo_time=dtTime, event_duration=EVENT_DURATION, child_geotype=GEOTYPE)
        o.save() 
        
    return render(request, 'geofence/geo_display.html', {'data':n})