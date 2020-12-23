This is my repo for the code and notes for the Pi Hut 3D Xmas tree

Basically, I followed the Pi Hut's tutorial exactly, then did some modifications of my own:
- setup to join network wherever I plan on placing it, so that it can determine the time
- modified python code to schedule on/off time
- setup a bash script to launch the python program, after providing sufficient delay for networking to be established, and to do some minimal logging that helped with dev
- set /etc/rc.local to kick off the bash script as part of the boot process


Timing:
- everything waits a full 90s to give networking a full chance at connection
- if the python program is able to confirm that it's on the network, it turns the xmas tree on (by default) at 5pm EST and off at 10pm EST
- if it cannot establish a network connection, it turns on immediately, and off 4hrs later, then repeats this sequence on a 24hr cycle.


user/pswd: pi/xmas

To get there from scratch: 
- Install fresh Raspberry Pi Os (can be "lite")
- setup for headless access
- put the device on the network, ssh to it (pi/raspberry)
- sudo apt-get update
- sudo apt-get upgrade
- sudo apt-get install xterm emacs git python-gpiozero

- install gpiozero (maybe requiring pip first?)

- git clone https://github.com/cicchiello/xmas.git
- cd xmas

- sudo cp etc/rc.local /etc/rc.local


I have an image that has everything I've described: /mnt/passport/RaspberryPi/2020-12-03-xmas.img

