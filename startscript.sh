#/bin/bash
sudo apt-get update
cd ~/IKO && git pull origin master
if $hostnamectl=rpi_1
then
        python3 write.py
fi
if $hostnamectl=rpi_2
then
        python3 read.py
fi
