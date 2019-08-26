<p align="center">
   <img alt="Linky" src="https://i.imgur.com/1WDZEWk.png" height="200" />
</p>

<h5 align="center"><i>Apache Tomcat credential checker</i></h5>

Simply, take a list of credentials from [SecLists](https://github.com/danielmiessler/SecLists/blob/master/Passwords/Default-Credentials/tomcat-betterdefaultpasslist.txt), and check them against a list of targets.

Quick note, Topcat cycles credential at a time,  rather than url at a time. This is so that each request for a given url is spaced out and not being hammered. 

*Currently no threading.*

#### Help Page

```
usage: topcat.py [-h] -t  -o

Topcat: Tomcat credential Checker

optional arguments:
  -h, --help       show this help message and exit
  -t , --targets   A file containing URLs/hostnames/IP Addresses
  -o , --output    File to output to (Only outputs as CSV)

python3 topcat.py --targets urls.txt --output sensible_filename.csv

```

#### Topcat in action

```
[06/08/19, 14:51:36] >> https://192.168.0.1/manager/html: Service Unavailable (503) ('QCC', 'QLogic66')
[06/08/19, 14:51:36] >> https://192.168.0.2/manager/html: Authorisation Failure (403) ('QCC', 'QLogic66')
[06/08/19, 14:51:37] >> https://192.168.0.3/manager/html: Page not found (404) ('QCC', 'QLogic66')
[06/08/19, 14:51:38] >> https://192.168.0.4/manager/html: Authentication Failure (401) ('QCC', 'QLogic66')
[06/08/19, 14:51:39] >> https://192.168.0.5/manager/html: Authentication Failure (401) ('QCC', 'QLogic66')
[06/08/19, 14:51:39] >> https://192.168.0.6/manager/html: Page not found (404) ('QCC', 'QLogic66')
[06/08/19, 14:51:39] >> https://192.168.0.7/manager/html: Page not found (404) ('QCC', 'QLogic66')
[06/08/19, 14:51:39] >> https://192.168.0.8/manager/html: Authentication Failure (401) ('QCC', 'QLogic66')
[06/08/19, 14:51:39] >> https://192.168.0.9/manager/html: Authentication Failure (401) ('role1', 'admanager')
[06/08/19, 14:51:40] >> https://192.168.0.10/manager/html: Authorisation Failure (403) ('role1', 'admanager')
[06/08/19, 14:51:41] >> https://192.168.0.11/manager/html: Authorisation Failure (403) ('role1', 'admanager')
[06/08/19, 14:51:42] >> https://192.168.0.12/manager/html: Authorisation Failure (403) ('role1', 'admanager')
```
