Vagrant::Config.run do |config|
  config.vm.box = "base"

  config.vm.network :hostonly, "33.33.33.33"

  config.vm.forward_port 80, 8080
  # Fix dns resolution - see http://lyte.id.au/tag/virtualbox/
  config.vm.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
  config.vm.customize ["modifyvm", :id, "--memory", "2048"]
end
