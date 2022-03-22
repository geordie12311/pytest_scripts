*** Settings ***
Library   ats.robot.pyATSRobot
Library   unicon.robot.UniconRobot

*** Test Cases ***

Connect to device
    use testbed "testbed.yaml"
    connect to all devices

Execute NTP Commands
    configure "username test priv 15 password test1" on all devices

Disconnect from device
    disconnect from all devices