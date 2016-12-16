# Cloud Foundry Application Lifecycle Management  
## Contents  
[1. Introduction](#1-introduction)   
[2. Dependencies](#2-dependencies)   
[3. Developing](#3-developing)  
[4. Preparing for Deployment](#4-preparing-for-deployment)  
[5. To push the applications](#5-to-push-the-applications)  
[6. Using the applications](#6-using-the-applications)  
[7. Creating some test applications](#7-creating-some-test-applications)  
[8. TODO](#8-todo)  
  
## 1. Introduction 
Shows application lifecycle metadata for all applications in a foundation, along with some basic information. The application is a  wrapper around the Cloud Controller's `/v2/organizations`, `/v2/spaces`, `/v2/apps`, `/v2/buildpacks` and `/v2/events` end points.  
  
Rather than asking each application to expose an end point, we adopt a convention, that every application's build pipeline must set  metadata that the organisation cares about via environment variables. In this example, a string called ALM_VERSION.  
  
The benefits of this approach is that it is very quick to retrieve information for all applications, and there is no onus on publishing applications to expose an additional end point.  
  
The drawback is that it is purely a convention, so there is nothing to stop someone changing the environment variables after the application is deployed.  
  
![Screenshot](https://github.com/bendalby82/cfalm/blob/master/images/testview.png)

## 2. Dependencies  
Python 2.7.10  
[Virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)    
  
## 3. Developing
### Status REST API
    
    cd appstatus  
    virtualenv venv  
    source venv/bin/activate  
    pip install requests  
    pip install Flask  
    
## 4. Preparing for Deployment  
### Status REST API  
    
    cd appstatus  
    source venv/bin/activate  
    mkdir -p vendor    
    pip freeze > requirements.txt    
    pip install --download vendor -r requirements.txt  
  
Note that `appstatus.py` currently has hard-coded domain and admin credentials for the Cloud Controller. These must be changed for your specific environment.  
  
### Status View Page  
    
    cf app appstatus | grep urls  
    #Edit line 31 of appstatusview/index.html to use the host and domain retrieved above.  
    
## 5. To push the applications  
### Status REST API
    
    cd appstatus
    cf push
    
### Status View Page  
    
    cd appstatusview
    cf push 
  
## 6. Using the applications  
REST API is visible at https://appstatus-host.DOMAIN/api/v1.0/apps  
Application view is visible at: http://appstatusview.DOMAIN/  
  
## 7. Creating some test applications
    
    cd appstatus
    ./CreateTestApps.sh

## 8. TODO  
a. appstatus: Remove hard-coded password (and externalise Cloud Controller domain)   
~~b. appstatusview: Externalise appstatus URL in Javascript fragment which is then easier to write to as part of deployment~~    
c. appstatusview: Add sorting to table  
d. appstatusview: Add different colour for 'CRASHED' status   
e. Both apps: Add support for pagination  
f. Add services  
~~g. Add buildpack file names~~  
