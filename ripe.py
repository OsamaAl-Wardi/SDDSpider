# --------------------------------------------------------------------------
# This code is a part of a Bachelor Thesis written by Osama Al-Wardi.
#
# Please refer to the repository https://github.com/OsamaAl-Wardi/SDDSpider
# for the latest version of SDDSpider.
#
# May 2020, Osama Al-Wardi, Bermen, Germany
# For question, please email osamaalwardi@yahoo.com
# --------------------------------------------------------------------------
import requests
import socket
import pprint
import json
from urllib.parse import urlparse
from colorama import Style, Fore, init

def ripe_lookup(base_url, output_dir = 'data/', verbose = True):
    base_url = urlparse(base_url)[1]
    ip = socket.gethostbyname(base_url)
    
    print (Style.BRIGHT + Fore.GREEN + '[+] ' + base_url + ' is resolved to ' + ip)
    print (Style.BRIGHT + Fore.GREEN + '[+] Requesting Information from the RIPEstat Data API')
    
    r = requests.get("https://stat.ripe.net/data/prefix-overview/data.json?resource="+str(ip))
    r2 = requests.get("https://stat.ripe.net/data/dns-chain/data.json?resource="+base_url)
    
    cont = json.loads(r.content.decode("utf-8"))
    cont2 = json.loads(r2.content.decode("utf-8"))
    
    if verbose:
        print (Style.BRIGHT + Fore.GREEN + '[+] Address Space Info \n')
        pprint.pprint(cont['data'])
        print (Style.BRIGHT + Fore.GREEN + '\n[+] Forward DNS Info \n')
        pprint.pprint(cont2['data'])
    
    print (Style.BRIGHT + Fore.GREEN + '[+] Saving the Results of the Prefix Lookup ' + output_dir + 'ripe_prefix.json')
    with open(output_dir + 'ripe_prefix.json', 'w') as file:
        json.dump(cont['data'], file)
        
    print (Style.BRIGHT + Fore.GREEN + '[+] Saving the Results of the Forward DNS Lookup ' + output_dir + 'ripe_dns.json')
    with open(output_dir + 'ripe_dns.json', 'w') as file:
        json.dump(cont2['data'], file)