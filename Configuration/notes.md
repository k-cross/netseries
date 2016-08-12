# Network Services Configuration Notes and Guides
## OpenVPN
* follow this http://readwrite.com/2014/04/10/raspberry-pi-vpn-tutorial-server-secure-web-browsing/

* Install OpenVPN and easy-rsa
* Copy all files from /usr/share/easy-rsa to a new dir /etc/openvpn/easy-rsa and cd to it
* Modify the 'vars' file
    * find and change 'export EASY_RSA="/etc/openvpn/easy-rsa"'
    * key size can also be changed if wanted
* Build a CA Certificate and Root CA certificate
    * Source the variables to the environment: 'source ./vars'
    * ./clean-all && ./build-ca
    * Don't really need to fill everything out
* ./build-key-server [Server_Name]
    * Keep all challenge passwords blank
* Build user keys with './build-key-pass UserName'
    * Enter PEM passphrase but keep challenge pw blank
* Encrypt the user keys
    * This needs to be done for android and ios devices
    * 'openssl rsa -in keyname.key -des3 -out keyname.3des.key'
* Generate Diffie-Hellman key exchange
    * ./build-dh
* DoS Protection by generating a hash-based message authentication code key (HMAC)
    * 'openvpn --genkey --secret keys/ta.key'
* Edit or make the /etc/openvpn/server.conf file
> local 192.168.2.0 # SWAP THIS NUMBER WITH YOUR IP ADDRESS
> dev tun 
> proto udp #Some people prefer to use tcp. Don't change it if you don't know.
> port 1194 
> ca /etc/openvpn/easy-rsa/keys/ca.crt 
> cert /etc/openvpn/easy-rsa/keys/Server.crt # SWAP WITH YOUR CRT NAME
> key /etc/openvpn/easy-rsa/keys/Server.key # SWAP WITH YOUR KEY NAME
> dh /etc/openvpn/easy-rsa/keys/dh1024.pem # If you changed to 2048, change that here!
> server 10.8.0.0 255.255.255.0 
> # server and remote endpoints 
> ifconfig 10.8.0.1 10.8.0.2 
> # Add route to Client routing table for the OpenVPN Server 
> push "route 10.8.0.1 255.255.255.255" 
> # Add route to Client routing table for the OpenVPN Subnet 
> push "route 10.8.0.0 255.255.255.0" 
> # your local subnet 
> push "route 192.168.2.0 255.255.255.0" # SWAP THE IP NUMBER WITH YOUR RASPBERRY PI IP ADDRESS
> # Set primary domain name server address to the SOHO Router 
> # If your router does not do DNS, you can use Google DNS 8.8.8.8 
> push "dhcp-option DNS 192.168.2.1" # This should already match your router address and not need to be changed.
> # Override the Client default gateway by using 0.0.0.0/1 and 
> # 128.0.0.0/1 rather than 0.0.0.0/0. This has the benefit of 
> # overriding but not wiping out the original default gateway. 
> push "redirect-gateway def1" 
> client-to-client 
> duplicate-cn 
> keepalive 10 120 
> tls-auth /etc/openvpn/easy-rsa/keys/ta.key 0 
> cipher AES-128-CBC 
> comp-lzo 
> user nobody 
> group nogroup 
> persist-key 
> persist-tun 
> status /var/log/openvpn-status.log 20 
> log /var/log/openvpn.log 
> verb 1
* Edit firewall rules and system rules to allow packet forwarding
    * For Raspberry Pi edit '/etc/sysctl.conf' and uncomment line for packet forwarding
    * After changing 'sysctl -p' reconfigures kernel parameters at runtime
    * Change firewall rules for raspbian by editing/creating /etc/firewall-openvpn-rules.sh
    * Add 'iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth0 -j SNAT --to-source IP_Addr'
    * 'chmod 700 firewall-openvpn-rules.sh && chown root /etc/firewall-openvpn-rules.sh'
* Edit interfaces
    * For pi its /etc/network/interfaces
    * Add '    pre-up /etc/firewall-openvpn-rules.sh' under 'iface eth0 inet dhcp'
* Reboot server
* Go to /etc/openvpn/easy-rsa/keys and make a Default.txt with a default client setup
* Create a MakeOVPN.sh script

> #!/bin/bash 
>  
> # Default Variable Declarations 
> DEFAULT="Default.txt" 
> FILEEXT=".ovpn" 
> CRT=".crt" 
> KEY=".3des.key" 
> CA="ca.crt" 
> TA="ta.key" 
>  
> #Ask for a Client name 
> echo "Please enter an existing Client Name:"
> read NAME 
>  
>  
> #1st Verify that client’s Public Key Exists 
> if [ ! -f $NAME$CRT ]; then 
>  echo "[ERROR]: Client Public Key Certificate not found: $NAME$CRT" 
>  exit 
> fi 
> echo "Client’s cert found: $NAME$CR" 
>  
>  
> #Then, verify that there is a private key for that client 
> if [ ! -f $NAME$KEY ]; then 
>  echo "[ERROR]: Client 3des Private Key not found: $NAME$KEY" 
>  exit 
> fi 
> echo "Client’s Private Key found: $NAME$KEY"
> 
> #Confirm the CA public key exists 
> if [ ! -f $CA ]; then 
>  echo "[ERROR]: CA Public Key not found: $CA" 
>  exit 
> fi 
> echo "CA public Key found: $CA" 
> 
> #Confirm the tls-auth ta key file exists 
> if [ ! -f $TA ]; then 
>  echo "[ERROR]: tls-auth Key not found: $TA" 
>  exit 
> fi 
> echo "tls-auth Private Key found: $TA" 
>  
> #Ready to make a new .opvn file - Start by populating with the 
> default file 
> cat $DEFAULT > $NAME$FILEEXT 
>  
> #Now, append the CA Public Cert 
> echo "<ca>" >> $NAME$FILEEXT 
> cat $CA >> $NAME$FILEEXT 
> echo "</ca>" >> $NAME$FILEEXT
> 
> #Next append the client Public Cert 
> echo "<cert>" >> $NAME$FILEEXT 
> cat $NAME$CRT | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' >> $NAME$FILEEXT 
> echo "</cert>" >> $NAME$FILEEXT 
>  
> #Then, append the client Private Key 
> echo "<key>" >> $NAME$FILEEXT 
> cat $NAME$KEY >> $NAME$FILEEXT 
> echo "</key>" >> $NAME$FILEEXT 
>  
> #Finally, append the TA Private Key 
> echo "<tls-auth>" >> $NAME$FILEEXT 
> cat $TA >> $NAME$FILEEXT 
> echo "</tls-auth>" >> $NAME$FILEEXT 
>  
> echo "Done! $NAME$FILEEXT Successfully Created."
> 
> #Script written by Eric Jodoin
> \ No newline at end of file
    * 'chmod 700 MakeOVPN.sh && ./MakeOVPN.sh'
    * Input your client name and look for 'Done! clientName.ovpn Succesfully Created.'


## Dynamic DNS
* Install ddclient and sign-up for a dynamic DNS service
* Configuration example for ddclient:
> daemon=600 #check ip every 600s
> protocol=dyndns2
> use=web, web=myip.dnsdynamic.org
> server=www.dnsdynamic.org
> login=yourun
> password='fill me'
> kurosawa.x64.me
* Run ddclient

## OpenWRT Configuration for Web Services
* Modify DNS settings
* Currently, modify /etc/config/uhttpd
    * change "list listen_http 0.0.0.0:80" to "list listen_http ip_of_webserver:80"
    * restart service
* Modify /etc/config/firewall
    * change redirect settings for port 80, or what's desired.
    * restart service

## Gitlab
* Change to HTTPS as default
    1. Modify /etc/gitlab.rb and change...
    2. Next run 'gitlab-ctrl reconfigure'
* Beware of hackers
    * Check access logs in /var/log/gitlab/nginx/gitlab_access.log
* TODO:
    * Keep hackers at bay by using something like fail2ban

## Optimizations
The whole ordeal is pretty slow and unreliable as is
* TODO
