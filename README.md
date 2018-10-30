# pythonsshattack
Brute force SSH credentials with python

Disclaimer

This programme is intended for education purposes only. I do not take any responsibility on how you use this programme.

Installation

Before using the programme please install paramiko

apt-get install python-paramiko


Usage

sshpwfinder.py [user] [target] [dictionary] [port] (optional, default=22) [threads](optional, default=9) Example: sshpwfinder.py root 192.168.1.123 passlist.txt
