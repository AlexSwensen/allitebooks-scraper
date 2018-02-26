# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.define "webscraper" do |webscraper|
    webscraper.vm.box = "ubuntu/xenial64"
    webscraper.vm.network "forwarded_port", guest: 80, host:8080
    webscraper.vm.network "private_network", ip: "10.0.0.10"
    webscraper.vm.network "public_network", use_dhcp_assigned_default_route: true
    webscraper.vm.hostname = "webscraper"
    webscraper.vm.synced_folder ".", "/vagrant"
        webscraper.vm.provider "virtualbox" do |vbw|
          vbw.gui = false
          vbw.memory = "1024"
        end
    webscraper.vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt upgrade -y
      apt-get install -y python3 python-pip
      sudo pip install --upgrade pip
      sudo pip install scrapy pymongo pipenv
      sudo ufw enable
      sudo ufw allow OpenSSH
     SHELL
    end
  end

  config.vm.define "mongodbserver" do |mongodbserver|
    mongodbserver.vm.box = "ubuntu/xenial64"
    mongodbserver.vm.network "forwarded_port", guest: 80, host:8080
    mongodbserver.vm.network "forwarded_port", guest:27017, host:27017
    mongodbserver.vm.network "private_network", ip: "10.0.0.11"
    mongodbserver.vm.network "public_network", use_dhcp_assigned_default_route: true
    mongodbserver.vm.hostname = "mongodbserver"
    mongodbserver.vm.provider "virtualbox" do |vbm|
      vbm.gui = false
      vbm.memory = "1024"
    end
    mongodbserver.vm.provision "shell", inline: <<-SHELL
      sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6 -y --allow-unauthenticated
      echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
      apt-get update
      apt upgrade -y
      apt-get install -y --allow-unauthenticated  mongodb-org
      sudo systemctl start mongod
      sudo systemctl status mongod
      sudo systemctl enable mongod
      mongo
      use admin
      db.createUser({user:"king",pwd:"lordpoopypants",roles:[{role:"userAdminAnyDatabase",db:"admin"}]})
      sudo sed 's/#security/security\n\tauthorization: "enabled"'/ /etc/mongod.conf
      sudo systemctl restart mongod
      sudo systemctl status mongod
      sudo ufw enable
      sudo ufw allow OpenSSH
      sudo ufw allow 27017
     SHELL
    end
  end
end