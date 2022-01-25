
# Project Description
This project is used on a raspberry pi that scans every 30 minutes to check if a certain MAC address is currently on the network. Basically, this script checks if a PC is powered ON or OFF.

## Video on how to use google sheet in python
since we are using google sheet to store data, google cloud platform is required. [Tutorial here](https://www.youtube.com/watch?v=cnPlKLEGR7E).

## Method to scan for PC status
* nmap - Using nmap to scan the network for existance of MAC address. Not very effective as not all available devices are picked up. process seemed slow too.
* scapy - Not all devices are discoverable, sometimes scanns return OFF when pc is ON

## TODOs
- [ ] A new method to scan network
