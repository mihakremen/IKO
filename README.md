# IKO
1) Make shure git is installed on Raspberry and ssh-key is deployed
2) Run: 

cd $HOME && git clone git@github.com:mihakremen/IKO.git \\ \
&& cd ~/IKO && chmod u+x startscript \\ \
&& crontab -e

5) In the end of the file add: \
@reboot ~/IKO/startscript

6) save file and exit
7) Run: \
sudo reboot
