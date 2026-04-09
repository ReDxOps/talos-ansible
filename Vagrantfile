Vagrant.configure("2") do |config|

  config.vm.box = "bento/debian-12"
  config.vm.box_check_update = false
  config.vm.box_version = "202510.26.0"
  config.vm.hostname = "talos-dev"
  #config.ssh.port = 8888 it's for vagrant command after bootstrap like "vagrant reload"

  config.vm.provider "vmware_desktop" do |vmware|
    vmware.memory = "4096"
    vmware.cpus = "2"
    vmware.gui = false
    vmware.allowlist_verified = true
    vmware.vmx["ethernet0.virtualDev"] = "vmxnet3"
  end

  config.vm.network "private_network", ip: "192.168.100.10"
  config.vm.synced_folder ".", "/vagrant"

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y python3 python3-pip python3-apt open-vm-tools open-vm-tools-desktop
  SHELL
end
