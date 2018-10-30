# pythonsshattack
Brute force SSH credentials with python

Installation

Before using the programme please install paramiko

apt-get install python-paramiko


Usage

sshpwfinder.py [user] [target] [dictionary] [port] (optional, default=22) [threads](optional, default=9) Example: sshpwfinder.py root 192.168.1.123 passlist.txt
