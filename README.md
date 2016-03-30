Ansible Automation Demo
=======================
This demo demonstrates how to write a manifest using Puppet to configure switches running Cumulus Linux and servers running Ubuntu. This manifest configures a CLOS topology running BGP numbered in the fabric with Layer 2 bridges to the hosts, and installs a webserver on one of the hosts to serve as a Hello World example. When the demo runs successfully, any server on the network should be able to access the webserver via the BGP routes established over the fabric.

This demo is written for the [cldemo-vagrant](https://github.com/cumulusnetworks/cldemo-vagrant) reference topology and applies the reference BGP numbered configuration from [cldemo-config-routing](https://github.com/cumulusnetworks/cldemo-config-routing).


Quickstart: Run the demo
------------------------
(This assumes you are running Ansible 1.9.4 and Vagrant 1.8.4 on your host.)

    git clone https://github.com/cumulusnetworks/cldemo-vagrant
    cd cldemo-vagrant
    vagrant up oob-mgmt-server oob-mgmt-switch leaf01 leaf02 spine01 spine02 server01 server02
    vagrant ssh oob-mgmt-server
    sudo su - cumulus
    git clone https://github.com/cumulusnetworks/cldemo-automation-puppet
    cd cldemo-automation-puppet
    sudo su
    wget https://apt.puppetlabs.com/puppetlabs-release-pc1-trusty.deb
    dpkg -i puppetlabs-release-pc1-trusty.deb
    apt-get update
    apt-get install puppetserver -qy
    rm -rf /etc/puppetlabs/code/environments/production
    ln -s  /home/cumulus/cldemo-automation-puppet/production /etc/puppetlabs/code/environments/production
    sed -i 's/-Xms2g/-Xms512m/g' /etc/default/puppetserver
    sed -i 's/-Xmx2g/-Xms512m/g' /etc/default/puppetserver
    service puppetserver restart
    exit
    python install-puppet-agents.py leaf01,leaf02,spine01,spine02,server01,server02
    ssh server01
    wget 172.16.2.101
    cat index.html

Topology Diagram
----------------
Not pictured below is our out-of-band management network from which we run Puppetserver.
The out of band management server runs DHCP and acts as the default gateway for all of
our devices out to the internet.

             +------------+       +------------+
             | spine01    |       | spine02    |
             |            |       |            |
             +------------+       +------------+
             swp1 |    swp2 \   / swp1    | swp2
                  |           X           |
            swp51 |   swp52 /   \ swp51   | swp52
             +------------+       +------------+
             | leaf01     |       | leaf02     |
             |            |       |            |
             +------------+       +------------+
             swp1 |                       | swp2
                  |                       |
             eth1 |                       | eth2
             +------------+       +------------+
             | server01   |       | server02   |
             |            |       |            |
             +------------+       +------------+



Configuring the puppetmaster
----------------------------
We will be installing our puppetmaster on `oob-mgmt-server`. We are going to
download the demo package, install the latest version of puppet, and create a
link in the puppet configuration directory to point to our puppet code instead.

    git clone https://github.com/cumulusnetworks/cldemo-automation-puppet
    cd cldemo-automation-puppet
    sudo su
    wget https://apt.puppetlabs.com/puppetlabs-release-pc1-trusty.deb
    dpkg -i puppetlabs-release-pc1-trusty.deb
    apt-get update
    apt-get install puppetserver -qy
    rm -rf /etc/puppetlabs/code/environments/production
    ln -s  /home/cumulus/cldemo-automation-puppet/production /etc/puppetlabs/code/environments/production

If running this on a virtual machine, open the file `/etc/default/puppetserver`
and configure the JVM to use 512 MB of RAM.

    JAVA_ARGS="-Xms512m -Xmx512m"

Start the puppetmaster.

    service puppetserver restart


Configuring the puppet agents
-----------------------------
Then configure the puppet agents on the switches and servers. Note that the
wget is to a different URL. Keep the puppetmaster open in a seperate terminal
window.

    sudo su
    wget https://apt.puppetlabs.com/pool/cumulus/PC1/p/puppetlabs-release-pc1/puppetlabs-release-pc1_0.9.4-1cumulus_all.deb
    dpkg -i puppetlabs-release-pc1_0.9.4-1cumulus_all.deb
    apt-get update
    apt-get install puppet-agent -qy
    echo 'server = oob-mgmt-server.lab.local' >> /etc/puppetlabs/puppet/puppet.conf
    /opt/puppetlabs/bin/puppet agent --test

This will create a certificate on the server that needs to be signed.

    # on the puppetmaster
    /opt/puppetlabs/bin/puppet cert list
    # find the name of the node
    /opt/puppetlabs/bin/puppet cert sign leaf01.lab.local

Back on the puppet agent, run the test command again.

    /opt/puppetlabs/bin/puppet agent --test

Assuming everything worked, run the following command to enable the puppet agent
in the background. Roughly every 30 minutes, the puppet agent will attempt to
query the puppetmaster for updated configuration. To force a client to update,
run the test command again.

    sudo service puppet start
