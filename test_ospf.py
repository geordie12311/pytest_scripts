#Python script to be used with pytest to test ospf connectivity
#you need to install the following packages: pytest, pytest-check, allure-pytest,
#genie (or pyats) as well as nornir and nornir-scrapli. Also you must disable loggining
#in the norninr config file (config.yaml) and create a pytest config file conftest.py
from nornir_scrapli.tasks import send_command
from nornir.core.filter import F
from pytest_check import check_func

NEIGHBOR_COUNT = {"Spine": 4, "Leaf": 6}
#neighbor count is where you set the expected number of ospf hosts based on the role you
#add in data in host.yaml for each host. In this case in the lab there is 4 spine switches and 
#there is 6 leaf. You can name them anything you like but this is where you set expected numbers

@check_func
def pullospf(task):
    my_list = []
    result = task.run(task=send_command, command="show ip ospf neighbor")
    task.host["facts"] = result.scrapli_response.genie_parse_output()
    interfaces = task.host["facts"]["interfaces"]
    for interface in interfaces:
        ospf_neighbor = interfaces[interface]["neighbors"]
        for key in ospf_neighbor:
            my_list.append(key)
    num_neighbors = len(my_list)
    role = task.host["role"]
    expected_neighbors = NEIGHBOR_COUNT[role]
    assert num_neighbors == expected_neighbors, f"{task.host} FAILED"
#function above is going to pull data from show ip ospf neighbor and use genie to 
#parse it as structured data. Tehn its going to validate number of neighors per host
#and then its going to validate the numbers against neighbor count and confirm if the
#numbers are as expected or not. If not it is going to tell you which host fails the test
def test_nornir(nr):
    nr.run(task=pullospf)