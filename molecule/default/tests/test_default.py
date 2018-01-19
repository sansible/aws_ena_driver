import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_driver_installed(host):
    cmd = host.run("modinfo ena -F version")
    assert cmd.stdout.find("1.5.0") is not -1
