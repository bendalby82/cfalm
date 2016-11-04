# cfalm
Show application lifecycle metadata for all applications in a foundation
## Developing
### Status REST API
    
    cd appstatus 
    
    
## Preparing for Deployment  
### Status REST API  
    
    mkdir -p vendor  
    pip freeze > requirements.txt  
    pip install --download vendor -r requirements.txt  

## To push applications  
### Status REST API
    
    
### Status View Page  
    
    cf push appstatusview -m 36M -b staticfile_buildpack 
  
Accessible at: http://appstatusview.local2.pcfdev.io/  
