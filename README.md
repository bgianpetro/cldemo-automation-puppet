Basic EVPN Demo
======================
This demo builds a basic EVPN topology using Puppet.  The motivation for this demo was to provide a simple EVPN configuration in order to provide support for VirtualBox (other Cumulus Linux EVPN demos are only supported on KVM because of their size)

This demo is written for the [cldemo-vagrant](https://github.com/cumulusnetworks/cldemo-vagrant) reference topology.  It uses a two leaf, two spine topology with BGP unnumbered running in the fabric.

Note that this project was originally forked from the [cldemo-automation-puppet](https://github.com/CumulusNetworks/cldemo-automation-puppet) repository in order to build the base Puppet configurations.  If you want to know more about how to configure the Puppet-specific aspects, please consult that project.


Run the demo
------------------------
Before running this demo, install [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds) and [Vagrant](https://releases.hashicorp.com/vagrant/). The currently supported versions of VirtualBox and Vagrant can be found on the [cldemo-vagrant](https://github.com/cumulusnetworks/cldemo-vagrant).

First get the Cumulux Linux demo topology: 

    git clone https://github.com/cumulusnetworks/cldemo-vagrant
    cd cldemo-vagrant

Because EVPN in Cumulus Linux requires version 3.3 or later, make sure the boxes have the proper version:

    sed -i 's/box_version = \"3\.2\.0\"/box_version = \"3.3.0\"/' Vagrantfile
   
Bring up the required devices in the topology:
 
    vagrant up oob-mgmt-server oob-mgmt-switch leaf01 leaf02 spine01 spine02 server01 server02
    vagrant ssh oob-mgmt-server
    sudo su - cumulus

Install Puppet and the required configurations:

    git clone https://github.com/bgianpetro/cldemo-basic-evpn
    cd cldemo-basic-evpn
    sudo su
    wget https://apt.puppetlabs.com/puppetlabs-release-pc1-xenial.deb
    dpkg -i puppetlabs-release-pc1-xenial.deb
    apt-get update
    apt-get install puppetserver -qy
    rm -rf /etc/puppetlabs/code/environments/production
    ln -s  /home/cumulus/cldemo-basic-evpn/ /etc/puppetlabs/code/environments/production
    sed -i 's/-Xms2g/-Xms512m/g' /etc/default/puppetserver
    sed -i 's/-Xmx2g/-Xmx512m/g' /etc/default/puppetserver
    service puppetserver restart
    exit
    python install-puppet-agents.py leaf01,leaf02,spine01,spine02,server01,server02


Topology Diagram
----------------
This demo runs on a spine-leaf topology with two single-attached hosts. Each device's management interface is connected to an out-of-band management switch and bridged with the out-of-band management server that runs the Puppetserver.

             +------------+       +------------+
             | spine01    |       | spine02    |
             |            |       |            |
             +------------+       +------------+
             swp1 |    swp2 \   / swp1    | swp2
                  |           X           |
            swp51 |   swp52 /   \ swp51   | swp52
             +------------+       +------------+
             | leaf01     |       | leaf02     |
             | (vtep)     |       | (vtep)     |
             +------------+       +------------+
             swp1 |                       | swp2
                  |                       |
             eth1 |                       | eth2
             +------------+       +------------+
             | server01   |       | server02   |
             |172.16.1.101|       |172.16.1.102|
             +------------+       +------------+

Validation
----------
On the leaves, make sure the BGP neighbors are up and are seeing routes (for both IPV4 and EVPN)

    net show bgp summ
    net show bgp
    net show bgp evpn route vni all

On server01, ping server02 and connect to its web server:
    
    ping 172.16.1.102
    curl 172.16.1.102
