#Python script to be used with pytest to test vlans
#you need to install the following packages: pytest, pytest-check, allure-pytest,
#genie (or pyats) as well as nornir and nornir-scrapli. Also you must disable loggining
#in the norninr config file (config.yaml) and create a pytest config file conftest.py
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml
from pytest_check import check_func

def load_vars(task):
    result = task.run(task=load_yaml, file=f"desired-state/vlans/{task.host}.yaml")
    loaded = result.result
#this function above is going to load yaml and then use the host specific var files held in
#/desired-state/vlans folder for each host as the benchmark data for testing against.
@check_func
def get_vlans(task):
    vlan_list = []
    result = task.run(task=send_command, command="show vlan")
    task.host["facts"] = result.scrapli_response.genie_parse_output()
    vlans = task.host["facts"]["vlans"]
    for vlan in vlans:
        if vlan in ["1", "1002", "1003", "1004", "1005"]:
            continue
        vlan_id = int(vlan)
        name = vlans[vlan]["name"]
        vlan_dict = {"id": vlan_id, "name": name}
        vlan_list.append(vlan_dict)
    expected = load_vars(task)["vlans"]
    assert expected == vlan_list, f"{task.host} FAILED"
#function above is going to pull data from show vlan and use genie to parse it as structured data. 
#Then its going to validate number of neighors per host. Then its going to validate the numbers 
#against the host specific var file and confirm if the vlans as per the host var files held in the 
#desired-state/vlan folder If not it is going to tell you which host fails the test
def test_vlan(nr):
    nr.run(task=get_vlans)