import sys
sys.path.append('../')
import appstatus
import pytest
import mock
import json
from pytest_mock import mocker 
from appstatus import CloudControllerConfig

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

def test_getallorgs_parses_api_call(mocker):
    mocker.patch.object(appstatus,'cf_curl_all')
    appstatus.cf_curl_all.return_value = json.loads('{"total_results": 2, "total_pages": 1, "prev_url": null, "next_url": null, "resources": [{"metadata": {"guid": "215468fd-b3a3-4cdd-9794-dd67869c0f44", "url": "/v2/organizations/215468fd-b3a3-4cdd-9794-dd67869c0f44", "created_at": "2017-01-30T13:38:43Z", "updated_at": "2017-01-30T13:38:43Z"}, "entity": {"name": "pcfdev-org", "billing_enabled": false, "quota_definition_guid": "fecd9c56-efce-4db9-b4bb-93bab4efd785", "status": "active", "default_isolation_segment_guid": null, "quota_definition_url": "/v2/quota_definitions/fecd9c56-efce-4db9-b4bb-93bab4efd785", "spaces_url": "/v2/organizations/215468fd-b3a3-4cdd-9794-dd67869c0f44/spaces", "domains_url": "/v2/organizations/215468fd-b3a3-4cdd-9794-dd67869c0f44/domains", "private_domains_url": "/v2/organizations/215468fd-b3a3-4cdd-9794-dd67869c0f44/private_domains", "users_url": "/v2/organizations/215468fd-b3a3-4cdd-9794-dd67869c0f44/users", "managers_url": "/v2/organizations/215468fd-b3a3-4cdd-9794-dd67869c0f44/managers", "billing_managers_url": "/v2/organizations/215468fd-b3a3-4cdd-9794-dd67869c0f44/billing_managers", "auditors_url": "/v2/organizations/215468fd-b3a3-4cdd-9794-dd67869c0f44/auditors", "app_events_url": "/v2/organizations/215468fd-b3a3-4cdd-9794-dd67869c0f44/app_events", "space_quota_definitions_url": "/v2/organizations/215468fd-b3a3-4cdd-9794-dd67869c0f44/space_quota_definitions"} }, {"metadata": {"guid": "2d0af448-fd8a-427a-b86c-7da3add55300", "url": "/v2/organizations/2d0af448-fd8a-427a-b86c-7da3add55300", "created_at": "2017-01-30T13:44:39Z", "updated_at": "2017-01-30T13:44:39Z"}, "entity": {"name": "system", "billing_enabled": false, "quota_definition_guid": "fecd9c56-efce-4db9-b4bb-93bab4efd785", "status": "active", "default_isolation_segment_guid": null, "quota_definition_url": "/v2/quota_definitions/fecd9c56-efce-4db9-b4bb-93bab4efd785", "spaces_url": "/v2/organizations/2d0af448-fd8a-427a-b86c-7da3add55300/spaces", "domains_url": "/v2/organizations/2d0af448-fd8a-427a-b86c-7da3add55300/domains", "private_domains_url": "/v2/organizations/2d0af448-fd8a-427a-b86c-7da3add55300/private_domains", "users_url": "/v2/organizations/2d0af448-fd8a-427a-b86c-7da3add55300/users", "managers_url": "/v2/organizations/2d0af448-fd8a-427a-b86c-7da3add55300/managers", "billing_managers_url": "/v2/organizations/2d0af448-fd8a-427a-b86c-7da3add55300/billing_managers", "auditors_url": "/v2/organizations/2d0af448-fd8a-427a-b86c-7da3add55300/auditors", "app_events_url": "/v2/organizations/2d0af448-fd8a-427a-b86c-7da3add55300/app_events", "space_quota_definitions_url": "/v2/organizations/2d0af448-fd8a-427a-b86c-7da3add55300/space_quota_definitions"} } ] }')
    orgdic = appstatus.getallorgs()
    assert orgdic['2d0af448-fd8a-427a-b86c-7da3add55300'] == 'system'
    assert orgdic['215468fd-b3a3-4cdd-9794-dd67869c0f44'] == 'pcfdev-org'
    assert len(orgdic)==2
