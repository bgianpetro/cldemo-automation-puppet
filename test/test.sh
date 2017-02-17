wget https://apt.puppetlabs.com/puppetlabs-release-pc1-xenial.deb
sudo dpkg -i puppetlabs-release-pc1-xenial.deb
sudo apt-get update
sudo apt-get install puppetserver -qy
sudo rm -rf /etc/puppetlabs/code/environments/production
sudo ln -s  /home/cumulus/cldemo-automation-puppet/ /etc/puppetlabs/code/environments/production
sudo service puppetserver restart
python install-puppet-agents.py leaf01,leaf02,spine01,spine02,server01,server02
ssh server01 wget -T 30 -t 1 172.16.2.101
ssh server01 cat index.html
