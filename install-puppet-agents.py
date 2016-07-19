#! /usr/bin/env python

# This script installs the puppet agent on the hosts specified in the command
# line arguments. This script assumes that the 'cumulus' user has passwordless
# sudo enabled on the target devices.

import sys
import paramiko
import time
import os
from paramiko import SSHClient
from multiprocessing import Process

def go(host):
    expect = paramiko.SSHClient()
    expect.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    expect.connect(host, username="cumulus", password="CumulusLinux!")

    for line in ['sudo wget https://apt.puppetlabs.com/pool/cumulus/PC1/p/puppetlabs-release-pc1/puppetlabs-release-pc1_1.0.0-2cumulus_all.deb',
                 'sudo dpkg -i puppetlabs-release-pc1_1.0.0-2cumulus_all.deb',
                 'sudo apt-get update',
                 'sudo apt-get install puppet-agent -qy',
                 "sudo echo 'server = oob-mgmt-server.lab.local' | sudo tee /etc/puppetlabs/puppet/puppet.conf -a",
                 'sudo /opt/puppetlabs/bin/puppet agent --test']:
        stdin, stdout, stderr = expect.exec_command(line, get_pty=True)
        stdout.channel.recv_exit_status()
        print("%s: %s"%(host, line))
    os.system('sudo /opt/puppetlabs/bin/puppet cert sign %s.lab.local'%host)
    for line in ['sudo /opt/puppetlabs/bin/puppet agent --test',
                 'sudo service puppet start']:
        stdin, stdout, stderr = expect.exec_command(line, get_pty=True)
        stdout.channel.recv_exit_status()
        print("%s: %s"%(host, line))
    expect.close()


if __name__ == "__main__":
    try:
        hostnames = sys.argv[1].split(',')
    except:
        print("Usage: install-puppet-agents.py [leaf01,leaf02,etc]")
        sys.exit(-1)

    processes = []
    for host in hostnames:
        p = Process(target=go, args=(host,))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
