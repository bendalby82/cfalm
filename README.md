# cfalm
Show application lifecycle metadata for all applications in a foundation  
## Dependencies  
Python 2.7.10  
Virtualenv  
  
## Developing
### Status REST API
    
    cd appstatus  
    virtualenv venv  
    source venv/bin/activate  
    pip install requests  
    pip install Flask  
    
## Preparing for Deployment  
### Status REST API  
    
    cd appstatus  
    source venv/bin/activate  
    mkdir -p vendor    
    pip freeze > requirements.txt    
    pip install --download vendor -r requirements.txt  

## To push applications  
### Status REST API
    
    cf push
    
### Status View Page  
    
    cf push appstatusview -m 36M -b staticfile_buildpack 
  
## Using the applications  
REST API is visible at https://appstatus-host.local2.pcfdev.io/  
Application view is visible at: http://appstatusview.local2.pcfdev.io/  
