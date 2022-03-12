#Python script to be used with pytest to test vlans
#you need to install the following packages: pytest, pytest-check, allure-pytest,
#genie (or pyats) as well as nornir and nornir-scrapli. Also you must disable loggining
#in the norninr config file (config.yaml) and create a pytest config file conftest.py
import pytest
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml

nr = InitNornir(config_file="config.yaml")

def get_vlans(task):
    vlan_list = []
    result = task.run(task=send_command, command="show vlan")
    task.host["vlan_details"] = result.scrapli_response.genie_parse_output()
#function above is going to pull data from show vlan and use genie to parse it as structured data. 
#Then its going to validate number of neighors per host. Then its going to validate the numbers 
#against the host specific var file and confirm if the vlans as per the host var files held in the 
#desired-state/vlan folder If not it is going to tell you which host fails the test

def load_vars(task):
    result = task.run(task=load_yaml, file=f"desired_state/vlans/{task.host}.yaml")
    task.host["loaded_vars"] = result.result

def get_device_names():
    devices = (nr.inventory.hosts.keys())
    return devices

class Testvlans:
    @pytest.fixture(scope="class", autouse=True)
    def setup_teardown(self, pytestnr)
    pytestnr.run(load_vars)
    pytestnr.run(get_vlans)
    yield
    for host in pytestnr.inventory.hosts.values():
        host.data.pop("vlan_data")
    
    @pytest.mark.parametrize("device_name", get_device_names())
    def test_vlans_consistency(self, pytestnr, device_name):
        vlan_list = []
        nr_host = pytestnr.inventory.hosts[device_name]
        expected_vlans = nr_host["loaded_vars"]["vlans"]
        vlans = nr_host["vlan_data"]["vlans"]
        for vlan in vlans:
            if vlan in ["1", "1002", "1003", "1004", "1005"]:
                continue
            vlan_id = int(vlan)
            name = vlans[vlan]["name"]
            vlan_dict = {"id": vlan_id, "name": name}
            vlan_list.append(vlan_dict)
        assert expected_vlans == vlan_list, f"{nr_host} FAILED"
#this is going to create an object called device_name and run the get_device_names function
#its going to use the results from load_vars and strip out the vlan information
#then it will ignore the default and reserved vlan number but compare the remaining vlans it 
#finds to compare agains the expected vlans in vlan_list. If they are not comparable it will
#flag the fact that the specific host has failed and provide details of the differences


