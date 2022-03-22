"""
test_connections.py and test_interface_errors.py

Verify that connection works to all hosts in the test bed and no errors have been reported on network interfaces.

"""
import os
from pyats.easypy import run

# compute the script path from this location
SCRIPT_PATH = os.path.dirname(__file__)


def main(runtime):
    """job file entrypoint"""

    # run scripts
    run(testscript=os.path.join(SCRIPT_PATH, "test_connections.py"), runtime=runtime)
    run(testscript=os.path.join(SCRIPT_PATH, "test_interface_errors.py"), runtime=runtime)
