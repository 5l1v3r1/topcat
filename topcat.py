#!/usr/bin/python3
import requests,sys,argparse, csv,os
from time import gmtime, strftime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

colour_red = "\033[1;31m"
colour_blue = "\033[1;34m"
colour_green = "\033[1;32m"
colour_yellow = "\033[1;33m"
colour_remove= "\033[0m"

def RED(string):
	string=str(string)
	return (colour_red + string + colour_remove)

def BLUE(string):
	string=str(string)
	return (colour_blue + string + colour_remove)

def GREEN(string):
	string=str(string)
	return (colour_green + string + colour_remove)

def YELLOW(string):
	string=str(string)
	return (colour_yellow + string + colour_remove)

def blue(string):
	log_time=strftime("%d/%m/%y, %H:%M:%S", gmtime())
	print('['+log_time+']'+BLUE(' >> ' )+string)

def green(string):
	log_time=strftime("%d/%m/%y, %H:%M:%S", gmtime())
	print('['+log_time+']'+GREEN(' >> ' )+string)

def red(string):
	log_time=strftime("%d/%m/%y, %H:%M:%S", gmtime())
	print('['+log_time+']'+RED(' >> ' )+string)

def yellow(string):
	log_time=strftime("%d/%m/%y, %H:%M:%S", gmtime())
	print('['+log_time+']'+YELLOW(' >> ' )+string)

def check_creds(host,creds):

	if host.endswith('/manager/html'):
		pass
	else:
		url = host + '/manager/html'
	username = creds.split(':')[0]
	password = creds.split(':')[1]
	auth = (username,password)

	headers = {
	"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
	 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	 "Accept-Language": "en-GB,en;q=0.5",
	 "Accept-Encoding": "gzip, deflate",
	 "Connection": "close",
	 "Upgrade-Insecure-Requests": "1"
	}

	if url.startswith('https://') or url.startswith('http://'):
		try:
			r=requests.get(url, headers=headers,auth=auth,verify=False,timeout=3)
		except Exception as e:
			red('%s timed out' % RED(url))
			return
	else:
		url = 'https://'+url
		try:
			r=requests.get(url, headers=headers,auth=auth,verify=False,timeout=3)
		except Exception as e:

			red('%s timed out' % RED(url))
			try:
				url = 'http://'+host
				r=requests.get(url, headers=headers,auth=auth,verify=False,timeout=3)
			except Exception as e:
				red('%s timed out' % RED(url))
				return
			return

	status_code = r.status_code

	AUTHENTICATION_FAIL = 'Authentication Failure'
	AUTHORISATION_FAIL = 'Authorisation Failure'
	NOT_FOUND = 'Page not found'
	SERVER_ERROR = 'Internal Server Error'
	SERVICE_UNAVAILABLE = 'Service Unavailable'
	SUCCESSFUL = 'Successful'
	UNKNOWN = 'Unknown Error'

	if status_code == 401:
		red('%s: %s (%s) %s' % (url,RED(AUTHENTICATION_FAIL),status_code,auth))
		return [url,status_code,AUTHENTICATION_FAIL]

	elif status_code == 403:
		yellow('%s: %s (%s) %s' % (url,YELLOW(AUTHORISATION_FAIL),status_code,auth))
		return [url,status_code,AUTHORISATION_FAIL]

	elif status_code == 404:
		red('%s: %s (%s) %s' % (url,RED(NOT_FOUND),status_code,auth))
		return [url,status_code,NOT_FOUND]

	elif status_code == 500:
		red('%s: %s (%s) %s' % (url,RED(SERVER_ERROR),status_code,auth))
		return [url,status_code,SERVER_ERROR]

	elif status_code == 503:
		red('%s: %s (%s) %s' % (url,RED(SERVICE_UNAVAILABLE),status_code,auth))
		return [url,status_code,SERVICE_UNAVAILABLE]


	elif status_code == 200:
		green('%s: %s (%s) %s' % (url,GREEN(SUCCESSFUL),status_code,auth))
		return [url,status_code,SUCCESSFUL]

	else:
		red('%s: %s'  % (UNKNOWN,status_code))
		return [url,status_code,UNKNOWN]

def get_creds():
	cur_dir=os.path.dirname(os.path.abspath(__file__))
	if args.creds == None:
		filename = cur_dir+'/creds.txt'
	else:
		filename = args.creds
	creds=[]
	try:
		with open(filename,'r') as f:
			x=f.read()
			y=x.split('\n')
			creds=y
		creds=list(filter(None,creds))
		return creds
	except:
		red('This tool requires creds.txt, or a specified creds file, with colon seperated username and passwords (admin:admin)')
		red('If you are specifying your own creds file, specify it with %s' % RED('--creds'))
		quit()

def get_targets():
	targets=[]
	try:
		with open(args.targets,'r') as f:
			x=f.read()
			y=x.split('\n')
			targets=y
		targets=list(filter(None,targets))
		return targets
	except:
		red('Couldnt open %s' % RED(args.targets))
		quit()


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Topcat: Tomcat credential Checker",epilog='python3 topcat.py --targets urls.txt --output sensible_filename.csv')
	parser.add_argument("-t", "--targets", metavar="", required=True, help="A file containing URLs/hostnames/IP Addresses")
	parser.add_argument("-o", "--output", metavar="", required=True, help="File to output to (Only outputs as CSV)")
	parser.add_argument("-c", "--creds", metavar="", help="Specify cred")
	args = parser.parse_args()

	targets = get_targets()
	creds = get_creds()

	output = args.output

	results = []

	# Originally, this was the other way around but it would just hammer the app. 
	#  This way, each request is spaced out because the credential list is looped over first.
	for cred in creds:
		for target in targets:
			try:
				response=check_creds(target,cred)
				results.append(response)
			except KeyboardInterrupt:
				yellow('CTRL+C detected!')
				quit()
	try:
		with open(output,'w') as f:
			writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			headers=['URL','Status Code','Message']
			writer.writerow(headers)
	except:
		red('Unable to write to %s' % args.output)
		quit()

	for r in results:
		try:
			url = r[0]
			status_code = r[1]
			message = r[2]
		except Exception as e:
			print(e)
			continue
		try:
			writer.writerow([url,status_code,message])
		except Exception as e:
			print(e)
			continue
	green('Done!')
