## **Magic DLP Bypass**


### Project description
Magic DLP Bypass it's a python script that exfiltrates data locally or remotely (using HTTP POST requests) bypassing DLP measures.


### Dependencies
You can install the following dependencies using the requests.txt file:
```pip3 install -r requirements.txt```

Additionally, you need  xdd and base64 binaries installed on linux system.


### Available options on the client (magicdlp.py)


![alt text](https://raw.githubusercontent.com/magichk/magicdlpbypass/master/images/magicdlpmenu.png "Magicdlp client - menu")


### Available options on the server, the server can receive the data remotely (server.py)


![alt text](https://raw.githubusercontent.com/magichk/magicdlpbypass/master/images/magicdlpmenuserver.png "Magicdlp server - menu")


### How it works ? Scenario 1
First of all, we will run the server.py script on the server where we store the exfiltrate data from the client.


![alt text](https://raw.githubusercontent.com/magichk/magicdlpbypass/master/images/magicdlpserverrunning.png "Magicdlp server running - server running")


Example of usage of Magic DLP Bypass client to send data remotely.


![alt text](https://raw.githubusercontent.com/magichk/magicdlpbypass/master/images/magicdlpclientrunning.png "Magicdlp client running - client running")


When the data is transfered we can see the POST requests on the webserver.
![alt text](https://raw.githubusercontent.com/magichk/magicdlpbypass/master/images/magicdlpserverrunning2.png "Magicdlp server running - server running")



### Windows Client


The magicdlp.ps1 it's a module for windows that works like the linux version and using the same server.py


![alt text](https://raw.githubusercontent.com/magichk/magicdlpbypass/master/images/magicdlpmenuwindows.png "Magicdlp windows client - windows client")


### Docker Support

The Dockerfile creates an image in order to execute the server.py script and wait for remote connections.

![alt text](https://raw.githubusercontent.com/magichk/magicdlpbypass/master/images/magicdlpserverdocker.png "Magicdlp docker server - docker server")
