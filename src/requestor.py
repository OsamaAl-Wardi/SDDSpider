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
import json
import pprint
from colorama import Style, Fore, init


def capture_requests(output_dir = '/data', verbose = True):
    data = {}

    print (Style.BRIGHT + Fore.GREEN + '[+] Requesting All Pages from ' + output_dir + 'resources.json')
    with open(output_dir + 'resources.json') as file:
        resources = json.load(file)
        resources = json.loads(resources)

    for url in resources:
        r = requests.get(url)
        data [url] = json.dumps(dict(r.headers))
    
    if verbose:
        print (Style.BRIGHT + Fore.GREEN + '[+] All HTTP/HTTPs Requests')
        pprint.pprint(data)
        
    data = json.dumps(data)
    
    print (Style.BRIGHT + Fore.GREEN + '[+] Saving All HTTP/HTTPs Communications in ' + output_dir + 'resources.json')
    with open(output_dir + 'requests.json', 'w') as file:
        json.dump(data, file)

    return data
