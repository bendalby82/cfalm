import os
from appstatus import appstatus
import pytest
import json
from pytest_mock import mocker 

def filetostring(myfilename):
    fqpn = os.path.dirname(os.path.realpath(__file__)) + '/' + myfilename
    myfile=open(fqpn,'r')
    myfilecontents=myfile.read()
    myfile.close()
    return myfilecontents

def test_no_vcap_env_var_fails():
    with pytest.raises(EnvironmentError) as e_info:
        appstatus.parse_vcap_services()

def test_arbitrary_json_loads_but_fails():
    with pytest.raises(EnvironmentError) as e_info:
        appstatus.load_config_from_json('{"name":"value"}')

def test_missing_cups_section_fails():
    with pytest.raises(EnvironmentError) as e_info:
        appstatus.load_config_from_json('{"user-provided":[{"name":"nothing"}]}')

def test_valid_json_loads():
    ccfg = appstatus.load_config_from_json('{"user-provided": [{"credentials": {"CFALM_CC_PWD": "admin","CFALM_CC_UID": "admin","CFALM_SYSTEM_DOMAIN": "local.pcfdev.io"},"syslog_drain_url": "","volume_mounts": [],"label": "user-provided","name": "cclink","tags": []}]}')
    assert ccfg.username == "admin"
    assert ccfg.password == "admin"
    assert ccfg.systemdomain == "local.pcfdev.io"

def test_missing_cups_called_cclinkfails():
    with pytest.raises(EnvironmentError) as e_info:
        appstatus.load_config_from_json('{"user-provided": [{"credentials": {"CFALM_CC_PWD": "admin","CFALM_CC_UID": "admin","CFALM_SYSTEM_DOMAIN": "local.pcfdev.io"},"syslog_drain_url": "","volume_mounts": [],"label": "user-provided","name": "NOTcclink","tags": []}]}')

def test_missing_username_fails():
    with pytest.raises(EnvironmentError) as e_info:
        appstatus.load_config_from_json('{"user-provided": [{"credentials": {"CFALM_CC_PWD": "admin","CFALM_SYSTEM_DOMAIN": "local.pcfdev.io"},"syslog_drain_url": "","volume_mounts": [],"label": "user-provided","name": "cclink","tags": []}]}')

def test_empty_username_fails():
    with pytest.raises(EnvironmentError) as e_info:
        appstatus.load_config_from_json('{"user-provided": [{"credentials": {"CFALM_CC_PWD": "admin","CFALM_CC_UID": "","CFALM_SYSTEM_DOMAIN": "local.pcfdev.io"},"syslog_drain_url": "","volume_mounts": [],"label": "user-provided","name": "cclink","tags": []}]}')

def test_missing_password_fails():
    with pytest.raises(EnvironmentError) as e_info:
        appstatus.load_config_from_json('{"user-provided": [{"credentials": {"CFALM_CC_UID": "admin","CFALM_SYSTEM_DOMAIN": "local.pcfdev.io"},"syslog_drain_url": "","volume_mounts": [],"label": "user-provided","name": "cclink","tags": []}]}')

def test_empty_password_fails():
    with pytest.raises(EnvironmentError) as e_info:
        appstatus.load_config_from_json('{"user-provided": [{"credentials": {"CFALM_CC_PWD": "","CFALM_CC_UID": "admin","CFALM_SYSTEM_DOMAIN": "local.pcfdev.io"},"syslog_drain_url": "","volume_mounts": [],"label": "user-provided","name": "cclink","tags": []}]}')

def test_missing_domain_fails():
    with pytest.raises(EnvironmentError) as e_info:
        appstatus.load_config_from_json('{"user-provided": [{"credentials": {"CFALM_CC_PWD": "admin","CFALM_CC_UID": "admin"},"syslog_drain_url": "","volume_mounts": [],"label": "user-provided","name": "cclink","tags": []}]}')

def test_empty_domain_fails():
    with pytest.raises(EnvironmentError) as e_info:
        appstatus.load_config_from_json('{"user-provided": [{"credentials": {"CFALM_CC_PWD": "admin","CFALM_CC_UID": "admin","CFALM_SYSTEM_DOMAIN": ""},"syslog_drain_url": "","volume_mounts": [],"label": "user-provided","name": "cclink","tags": []}]}')

def test_getallorgs_parses_valid_api_response(mocker):
    mocker.patch.object(appstatus,'cf_curl_all')
    jsonquery=filetostring("orgs.json")
    appstatus.cf_curl_all.return_value = json.loads(jsonquery)
    orgdic = appstatus.getallorgs()
    assert orgdic['2d0af448-fd8a-427a-b86c-7da3add55300'] == 'system'
    assert orgdic['215468fd-b3a3-4cdd-9794-dd67869c0f44'] == 'pcfdev-org'
    assert len(orgdic)==2

def test_getallspaces_parses_valid_api_response(mocker):
    mocker.patch.object(appstatus,'cf_curl_all')
    jsonquery=filetostring("spaces.json")
    appstatus.cf_curl_all.return_value = json.loads(jsonquery)
    spacedic = appstatus.getallspaces()
    assert spacedic['35248c13-306b-4058-9a95-7154fd8fda5b']['space_name']=='system'
    assert spacedic['35248c13-306b-4058-9a95-7154fd8fda5b']['organization_guid']=='2d0af448-fd8a-427a-b86c-7da3add55300'
    assert len(spacedic)==2

def test_getallapps_parses_valid_api_response(mocker):
    mocker.patch.object(appstatus,'cf_curl_all')
    jsonquery=filetostring("apps.json")
    appstatus.cf_curl_all.return_value = json.loads(jsonquery)
    allapps = appstatus.getallapps()
    assert len(allapps["resources"])==4

def test_getallbuildpacks_parses_valid_api_response(mocker):
    mocker.patch.object(appstatus,'cf_curl_all')
    buildpackquery=filetostring("buildpacks.json")
    appstatus.cf_curl_all.return_value = json.loads(buildpackquery)
    allbps = appstatus.getallbuildpacks()
    assert len(allbps)==9
    assert allbps["f9c88f20-6a5c-4c8f-abd7-e6193c99dc11"]=="dotnet-core_buildpack-cached-v1.0.5.zip"