# Network Services Configuration Notes and Guides
## OpenVPN
* follow this http://readwrite.com/2014/04/10/raspberry-pi-vpn-tutorial-server-secure-web-browsing/

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

## Optimizations
The whole ordeal is pretty slow and unreliable as is
* TODO
