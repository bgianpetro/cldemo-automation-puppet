#! /usr/bin/env python

import sys
import paramiko
import time
import os
from paramiko import SSHClient
from multiprocessing import Process

def go(host):
    url = "http://oob-mgmt-server.lab.local/cldemo-config-routing/%s/"%demo
    expect = paramiko.SSHClient()
    expect.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    expect.connect(host, username="cumulus", password="CumulusLinux!")
    stdin, stdout, stderr = expect.exec_command("sudo su", get_pty=True)
    for line in ['CumulusLinux!',
                 'wget https://apt.puppetlabs.com/pool/cumulus/PC1/p/puppetlabs-release-pc1/puppetlabs-release-pc1_0.9.4-1cumulus_all.deb',
                 'dpkg -i puppetlabs-release-pc1_0.9.4-1cumulus_all.deb',
                 'apt-get update',
                 'apt-get install puppet-agent -qy',
                 "echo 'server = oob-mgmt-server.lab.local' >> /etc/puppetlabs/puppet/puppet.conf",
                 '/opt/puppetlabs/bin/puppet agent --test']:
        print("%s: %s"%(host, line))
        stdin.write('%s\n'%line)
        stdin.flush()
        time.sleep(2)
    os.system('sudo /opt/puppetlabs/bin/puppet cert sign %s.lab.local'%host)
    for line in ['/opt/puppetlabs/bin/puppet agent --test']:
        print("%s: %s"%(host, line))
        stdin.write('%s\n'%line)
        stdin.flush()
        time.sleep(2)
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
