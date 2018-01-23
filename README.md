# Geofence_Vehicle-Tracking-System
## Motivation
Geofence is a virtual barrier for a real-world geographic area that triggers when vehicles enter or exit. Geofencing is used as a location-aware device that alert and notify managers when their vehicles enter or exit permitted or unpermitted areas. As a result, managers can monitor driver behaviors and vehicles' activities. 

![alt text](https://user-images.githubusercontent.com/30711638/35192107-3b5d637c-fe59-11e7-9f4f-34416acaa4b9.png) 

## Implementation
The concept of geofence sounds really simple, yet its implementation can be tricky and complicated because it deals with many parties and communication channels. 
1. The managers draw their desired geofence areas 
2. The companies must register their desired geofences and their vehicles with Aviation Park Staging Ground (APSG) of Singapore. (This is the most troublesome step)
3. Every time a vehicle enters or exits the registered geofence, its **GPS tracker sends a signal to the Middleware**
4. Simultaneously, **the Middleware notifies the APSG site that the registered vehicle entered or exited the registered geofence**
5. The APSG site would check if the vehicle that sends the request is registered in the corresponding geofence. After all conditions are satisfied, **the APSG site would send back a "Okay" message to the Middleware** and **the Middleware allows the vehicle to enter or exit the geofence**

As you realize from the process above, there are many
My Geofence project at Skyfy Technology is writing a middleware that handle 

![alt text](https://user-images.githubusercontent.com/30711638/35197869-443ab886-feb4-11e7-96b9-3e4dcba0971b.png)
## Database Desgin
![alt text](https://user-images.githubusercontent.com/30711638/35198038-d2918c3e-feb6-11e7-8f91-4753900fb97d.png)
![alt text](https://user-images.githubusercontent.com/30711638/35291824-995052de-003c-11e8-8787-47dff466da06.png)
## Prerequisites
- [Django](https://www.djangoproject.com/download/)
- [MySQL](https://www.mysql.com/)
- [Python](https://www.python.org/downloads/)
-
