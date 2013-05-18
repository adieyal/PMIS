# Install provisioning required packages
pip install -r requirements/provisioning.txt

# Download and install vagrant
wget -O /tmp/vagrant_1.2.1_x86_64.deb http://files.vagrantup.com/packages/a7853fe7b7f08dbedbc934eb9230d33be6bf746f/vagrant_1.2.1_x86_64.deb
sudo dpkg -i /tmp/vagrant_1.2.1_x86_64.deb

# Download and install virtualbox
wget -O /tmp/virtualbox-4.2_4.2.12-84980~Ubuntu~quantal_amd64.deb http://download.virtualbox.org/virtualbox/4.2.12/virtualbox-4.2_4.2.12-84980~Ubuntu~quantal_amd64.deb
sudo dpkg -i /tmp/virtualbox-4.2_4.2.12-84980~Ubuntu~quantal_amd64.deb

# Use Ubuntu 12.04 base image and make vm
vagrant box add base http://files.vagrantup.com/precise64.box
vagrant up

# Install the correct virtualbox additions
vagrant plugin install vagrant-vbguest
