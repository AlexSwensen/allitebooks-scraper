# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"
  config.vm.hostname = "MongoDb"

  # config.vm.box_check_update = false

  # config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 27017, host: 27017 #mongodb
  #config.vm.network "forwarded_port", guest: 27017, host: 27017
  #config.vm.network "forwarded_port", guest: 27017, host: 27017

  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 27017, host: 27017, host_ip: "127.0.0.1"

  # config.vm.network "private_network", ip: "192.168.33.10"

  config.vm.network "public_network"

  config.vm.synced_folder "C:/Users/drmaq/Documents/Workspace/allitebooks-scraper", "/allitebooks-scraper"

  config.vm.provider "virtualbox" do |vb|

     vb.gui = false
     vb.memory = "1024"
   end

  config.vm.provision "shell", inline: <<-SHELL
    mkdir /home/vagrant/allitebooks-scraper
    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6 -y --allow-unauthenticated

    echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list

    apt-get update
    apt upgrade -y

    apt-get install -y --allow-unauthenticated  mongodb-org
    apt-get install -y python3 python-pip
    sudo pip install --upgrade pip
    sudo pip install scrapy pymongo pipenv

    sudo systemctl start mongod
    sudo systemctl status mongod
    sudo systemctl enable mongod
    mongo
    db.createUser({user:"king",pwd:"lordpoopypants",roles:[{role:"userAdminAnyDatabase",db:"admin"}]})

    sudo ufw enable
    sudo ufw allow OpenSSH
    sudo ufw allow 27017

  SHELL
end
