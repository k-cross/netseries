# File Listings
## TCP Client
* tcp_client.py
* Simple client that accepts sends a tcp request expecting a response.
    * Python 3
## UDP Client
* udp_client.py
* Simple client that accepts sends data to localhost and tries to receive it.
    * Python 3
## RFC Downloader
* rfc_dl.py
* Just downloads a simple RFC Document
    * Python 3
## SSH
* ssh_client.py, ssh_server.py
* The client is a simple utility that acts as a very basic SSH client which can be modified
	* Python 3 - Using the Paramiko library for a SSH2 implementation
	* Currently does not give a shell, just streams simple commands
* The server is also a simple server, it currently doesn't handle much else than simple commands
	* Python 3 - Using the Paramiko library for a SSH2 implementation
