import argparse, sys, shodan, ipaddress

from colorama import init
from termcolor import colored
from censys.search import CensysHosts

ShodankeyString = 'shodan_api'
ShodanApi = shodan.Shodan(ShodankeyString)

def checkip(ip):
	try:
		ipaddress.ip_address(ip)
		return True
	except ValueError:
		return False

def checkzoomeye(ip):
	pass

def checkcensys(ip):
	print (colored("CENSYS", 'yellow'))
	h = CensysHosts()
	# Fetch a specific host and its services
	host = h.view(ip)
	print(host)
	meta = h.metadata()
	print(meta.get("services"))

def checkshodan(ip):
	print (colored("SHODAN", 'yellow'))
	try:
		host = ShodanApi.host(ip)
		print ("IP: ", colored(host['ip_str'], 'blue', attrs=['bold', 'blink']))
		print ('Organization: %s '  % host.get('org', 'n/a'))
		print ('OS: %s '  % host.get('os', 'n/a'))
		for item in host['data']:
			print ("Port:", colored(item['port'], 'red', attrs=['bold', 'blink']))
			print ("Banner:", item['data'])
	except:
		print(ip, "is not valid ip")



def searchip(ip):
	checkshodan(ip)
	#checkcensys(ip)
	#checkzoomeye(ip)
	pass
def readfile(filename):
	file = open(filename, 'r')
	ips = file.readlines()
	count = 0
	for ip in ips:
		count += 1
		if checkip(ip.strip()) == False:
			print(ip.strip(), "is not valid ip")
			exit()
		searchip(ip.strip())


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", help="Ip to check reputation")
	parser.add_argument("-l", help="List of ip to check reputation")
	args = parser.parse_args()
	if args.l:
		readfile(args.l)
		exit()
	if checkip(args.i) == False:
		print(args.i, "is not valid ip")
		exit()
	searchip(args.i)

main()
