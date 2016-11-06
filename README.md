# Cloud Foundry Application Lifecycle Management  
## Contents  
0. Introduction   
1. Dependencies   
2. Developing  
3. Preparing for Deployment  
4. To push the applications  
5. Using the applications  
6. Creating some test applications  
7. TODO  
  
## 0. Introduction 
Show application lifecycle metadata for all applications in a foundation, along with some basic information. The application is a simple wrapper around the Cloud Controller's `/v2/organizations`, `/v2/spaces` and `/v2/apps` end points.  
  
Rather than asking each application to expose an end point, we adopt a convention, that every application's build pipeline must set  metadata that the organisation cares about via environment variables. In this example, a string called ALM_VERSION.  
  
The benefits of this approach is that it is very quick to retrieve information for all applications, and there is no onus on publishing applications to expose an additional end point.  
  
The drawback is that it is purely a convention, so there is nothing to stop someone changing the environment variables after the application is deployed.  
  
![Screenshot](https://github.com/bendalby82/cfalm/blob/master/images/testview.png)

## 1. Dependencies  
Python 2.7.10  
[Virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)    
  
## 2. Developing
### Status REST API
    
    cd appstatus  
    virtualenv venv  
    source venv/bin/activate  
    pip install requests  
    pip install Flask  
    
## 3. Preparing for Deployment  
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
    
## 4. To push the applications  
### Status REST API
    
    cf push
    
### Status View Page  
    
    cf push appstatusview -m 16M -b staticfile_buildpack 
  
## 5. Using the applications  
REST API is visible at https://appstatus-host.DOMAIN/api/v1.0/apps  
Application view is visible at: http://appstatusview.DOMAIN/  
  
## 6. Creating some test applications
    
    cd appstatus
    ./CreateTestApps.sh

## 7. TODO  
a. appstatus: Remove hard-coded password (and externalise Cloud Controller domain)   
b. appstatusview: Externalise appstatus URL in Javascript fragment which is then easier to write to as part of deployment   
c. appstatusview: Add sorting to table  
d. appstatusview: Add different colour for 'CRASHED' status   
e. Both apps: Add support for pagination   
