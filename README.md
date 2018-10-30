# pythonsshattack
Brute force SSH credentials with python

Disclaimer

This programme is intended for education purposes only. I do not take any responsibility on how you use this programme.

Installation

Before using the programme please install paramiko

apt-get install python-paramiko


Usage

sshpwfinder.py [user] [target] [dictionary] [port] (optional, default=22) [threads](optional, default=9) Example: sshpwfinder.py root 192.168.1.123 passlist.txt

This programme can be used to carry out a dictionary attack or a brute force attack on an SSH service. To carry out a brute force attack please use my brute force dictionary generator found here: https://github.com/cyber-jack/bruteforcegen


Refrences: https://null-byte.wonderhowto.com/how-to/sploit-make-ssh-brute-forcer-python-0161689/
