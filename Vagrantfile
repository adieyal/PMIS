Vagrant.configure("1") do |config|
  config.vm.box = "base"
  config.vm.network :hostonly, "33.33.33.33"
  config.vm.forward_port 80, 8080

  # Fix dns resolution - see http://lyte.id.au/tag/virtualbox/
  config.vm.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
  config.vm.customize ["modifyvm", :id, "--memory", "2048"]

  config.vm.share_folder 'pmis', '/home/pmis/deploy', '.', :create => true, :owner => 'www-data', :group => 'www-data'
end

Vagrant.configure("2") do |config|
  config.vm.provision :ansible do |ansible|
    ansible.playbook = 'provisioning/playbook.yml'
    ansible.inventory_file = 'provisioning/ansible_hosts'
    ansible.verbose = true
  end
end
