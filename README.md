# usbswitch
Command line tool for USB switch device  
Tested on  
PC running Debian 10  
Raspberry Pi 3B  
so far...  

Works with  
Antrax Switchbox USB  
Cleware USB Switch
and probably some more...  

Calling arguments:  
-n 12345 : Serial number of the device, default: first found device  
-a 0 : switch on  
-a 1 : switch off  
-d : Show additional information  
-l : Just changing the light, no switching  
-r : No LED change  
-i : Reset the device before switching  
-s : Check after switching  
-h : Help  

Cooking receipt for Installation, extensive and safe:  
[assuming you are in you home directory]  
sudo apt update  
sudo apt upgrade  
mkdir pythonrun  
cd pythonrun  
[Now you put source files here]  
mkdir usbswitch  
cd usbswitch  
sudo apt-get install python3-venv  
python3 -m venv env  
source env/bin/activate  
pip install --upgrade pip  
pip install pyusb  
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="0d50", ATTRS{idProduct}=="0008", MODE="0666"' | sudo tee /etc/udev/rules.d/60-usbswitch.rules  
replug the USB connection...  

Cooking receipt for running to tool:  
cd ~/pythonrun/usbswitch  
source env/bin/activate  
[Now you can try:]  
python usbswitch.py -a 1  
[Switch on]  
python usbswitch.py -a 0  
[Switch off]  
python usbswitch.py -h  
[Get help]  

