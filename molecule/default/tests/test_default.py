import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    # Assert /etc/hosts exists,...
    f = host.file('/etc/hosts')
    assert f.exists
    # ...is owned by the user root,...
    assert f.user == 'root'
    # ...and owned by the group root.
    assert f.group == 'root'

# See http://testinfra.readthedocs.io/ for guidance on writing testinfra tests.
