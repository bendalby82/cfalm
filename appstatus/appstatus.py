# Name:           appstatus.py
#
# Dependencies:   Requests must be available on the machine, either via pip or unzipped to
#                 the same folder or the parent folder.
#!flask/bin/python
from flask import Flask, jsonify, request

app = Flask(__name__)

import sys, os

#These lines are necessary if we are running the script from cron
#They allow us to place libraries either in the same folder or the parent
sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0])))
sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0]))+'/..')

#Internal libaries
import json
import subprocess
import time

#Third party libraries
import requests

#Stores the access token for the duration of script execution
access_token = ""

#Credentials to retrieve token from UAA
systemdomain = ""
username = ""
password = ""

#The name of the user-provided service that will hold our link to the Cloud Controller
cupsname = "cclink"

#Attempt to retreive credentials from the above
if "VCAP_SERVICES" in os.environ:
    vcap = json.loads(os.environ["VCAP_SERVICES"])
    if "user-provided" in vcap:
        cclinkfound = False
        for cups in vcap["user-provided"]:
            if cups["name"] == cupsname:
                cclinkfound = True
                envkey = "CFALM_SYSTEM_DOMAIN"
                if envkey in cups["credentials"]:
                    systemdomain = cups["credentials"][envkey]
                else:
                    raise EnvironmentError("User-provided service %s is missing required property %s." % (cupsname,envkey))
                envkey = "CFALM_CC_UID"
                if envkey in cups["credentials"]:
                    username = cups["credentials"][envkey]
                else:
                    raise EnvironmentError("User-provided service %s is missing required property %s." % (cupsname,envkey))
                envkey = "CFALM_CC_PWD"
                if envkey in cups["credentials"]:
                    password = cups["credentials"][envkey]
                else:
                    raise EnvironmentError("User-provided service %s is missing required property %s." % (cupsname,envkey))
                break
        if not cclinkfound:
            raise EnvironmentError("No user-provided service called %s in VCAP_SERVICES." % cupsname)
    else:
        raise EnvironmentError("No user-provided service section in VCAP_SERVICES.")
else:
    raise EnvironmentError("VCAP_SERVICES environment variable not present.")

#Must be false in situations where host certificate is not trusted.
sslvalidation = False

def get_new_access_token(systemdomain, username, sslvalidation):
    qry = "https://uaa.%s/oauth/token" % systemdomain
    payload = {'username': username, 'password': password, 'grant_type': 'password'}
    headers = {'AUTHORIZATION': 'Basic Y2Y6'}
    r = requests.post(qry, data=payload, headers=headers, verify=sslvalidation)
    #Throw error if something went wrong
    r.raise_for_status()
    return r.json()["access_token"]

#Set sslvalidation=False to skip SSL Validation. Singleton for scope of script.
def get_access_token():
    global access_token
    #if not access_token:
    access_token = get_new_access_token(systemdomain, username, sslvalidation)
    return access_token

def cf_curl_get(url):
    headers = {'Authorization': 'bearer %s' % get_access_token(), 'Host': 'api.%s' % systemdomain, 'Cookie': ''}
    qry = "https://api.%s%s" % (systemdomain, url)
    #print >> sys.stderr, 'cf_curl_get: Calling: %s' % qry
    r = requests.get(qry, headers=headers, verify=sslvalidation)
    r.raise_for_status()
    return r.json()

#Given an arbitrary API call, will assemble paginated results into single result
def cf_curl_all(url):
    alldata = cf_curl_get(url)
    next_url = alldata["next_url"]
    while next_url:
        moredata = cf_curl_get(next_url)
        alldata["resources"] = alldata["resources"] + moredata["resources"]
        next_url = moredata["next_url"]
    return alldata

def getallorgs():
    qry = "/v2/organizations"
    allorgs = cf_curl_all(qry)
    orgdic={}
    for org in allorgs["resources"]:
        guid = org["metadata"]["guid"]
        orgdic[guid] = org["entity"]["name"]
    return orgdic

def getallspaces():
    qry = "/v2/spaces"
    allspaces=cf_curl_all(qry)
    spacedic = {}
    for space in allspaces["resources"]:
        guid = space["metadata"]["guid"]
        spacedic[guid]={'space_name':space["entity"]["name"],'organization_guid':space["entity"]["organization_guid"]}
    return spacedic

def getallapps():
    qry = "/v2/apps"
    allapps = cf_curl_all(qry)
    return allapps

def getallbuildpacks():
    qry = "/v2/buildpacks"
    allbuildpacks = cf_curl_all(qry)
    bpdic={}
    for bp in allbuildpacks["resources"]:
        guid = bp["metadata"]["guid"]
        bpdic[guid] = bp["entity"]["filename"]
    return bpdic

def getappcreationevents():
    qry = "/v2/events?q=type%20IN%20audit.app.create"
    allcreateevents = cf_curl_all(qry)
    #Build dictionary of app_guid:created_by
    acedic={}
    for ace in allcreateevents["resources"]:
        app_guid = ace["entity"]["actee"]
        acedic[app_guid] = ace["entity"]["actor_name"]
    return acedic

def getappdata():
    orgdic = getallorgs()
    spacedic = getallspaces()
    allapps = getallapps()
    allbuildpacks=getallbuildpacks()
    allcreateevents=getappcreationevents()
    outputlist = []
    for app in allapps["resources"]:
        listentry = {}
        app_guid = app["metadata"]["guid"]
        listentry["app_name"] = app["entity"]["name"]
        space_guid = app["entity"]["space_guid"]
        listentry["space_name"] = spacedic[space_guid]["space_name"]
        listentry["instances"] = app["entity"]["instances"]
        listentry["state"] = app["entity"]["state"]
        
        #Use ORG guid from space dictionary to key into ORG dictionary, which is
        #simple key-value pair of ORG_GUID: ORG_NAME
        listentry["org_name"] = orgdic[spacedic[space_guid]["organization_guid"]]
        if app["entity"]["buildpack"]:
            listentry["buildpack"] = app["entity"]["buildpack"]
        else: 
            listentry["buildpack"] = "%s (auto)" % app["entity"]["detected_buildpack"]

        listentry["buildpackfile"] = "-"
        #App will still list GUID if buildpack has been deleted.
        app_buildpack_guid = app["entity"]["detected_buildpack_guid"]
        if app_buildpack_guid:
            if app_buildpack_guid in allbuildpacks:
                listentry["buildpackfile"]=allbuildpacks[app_buildpack_guid]
            else:
                listentry["buildpackfile"]="Cannot retreive filename - GUID %s is not found via Buildpacks API" % app_buildpack_guid
        
        listentry["createdby"] = "-"
        if app_guid in allcreateevents:
            listentry["createdby"] = allcreateevents[app_guid]

        #Flatten environment JSON
        envjson = app["entity"]["environment_json"]
        for key, value in envjson.iteritems():
            listentry[key] = value  
        outputlist.append(listentry)
    return outputlist

#DEBUG CODE
def serializeheaders(mydic):
    headerstring = ""
    for k, v in mydic.items():
        if headerstring == "":
            headerstring = "%s:%s" % (k,v)
        else:
            headerstring = "%s,%s:%s" % (headerstring,k,v)
    return headerstring

@app.route('/api/v1.0/apps', methods=['GET'])
def get_tasks():
    #print serializeheaders(request.headers)
    return jsonify(getappdata())

@app.route('/', methods=['GET'])
def get_base():
    return 'Hello! API is located at <a href="/api/v1.0/apps">/api/v1.0/apps</a>'

@app.after_request
def after_request(response):
    #Allows us to call this from other domains.
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()
    app.run(host='0.0.0.0',port=8080)
