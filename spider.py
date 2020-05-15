import os
import json
import pprint
from colorama import Style, Fore, init
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions

def spider(base_url, output_dir = 'data/', verbose = True):
    # Setting Browser Options
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(executable_path='chromedriver', chrome_options=options)
    # Initializing Spider Variables
    links = []
    pages = {}
    # Opening Browser Window
    print (Style.BRIGHT + Fore.YELLOW + '[!] Browser Started. Browse Through the Website Normally!')
    print (Style.BRIGHT + Fore.YELLOW + '[!] Spider Started. Press ctrl + c to Stop Spidering!')
    browser.get(base_url)
    current_url = base_url
    spiderweb = [current_url]
    # Starting Spider
    print (Style.BRIGHT + Fore.GREEN +'[+] Page Opened, Anaylsing the DOM Tree. Please Continue Browsing!')
    print (Style.BRIGHT + Fore.GREEN + '[+] Capturing all hrefs, images and scripts')
    while True:
        # Checking if new page was opened
        if browser.current_url != current_url:
            print (Style.BRIGHT + Fore.GREEN +'[+] New Page Opened, Anaylsing the DOM Tree. Please Continue Browsing!')
            print (Style.BRIGHT + Fore.GREEN + '[+] Capturing all hrefs, images and scripts')
            current_url = browser.current_url
            spiderweb.append(current_url)
            links = []
            
        try:
            # Finding all Links, Images and Scripts without duplicates
            element = browser.find_elements_by_xpath('//*[@href]')
            img = browser.find_elements_by_tag_name('img')
            script = browser.find_elements_by_tag_name('script')
            
            
            for i in element:
                if i.get_attribute('href') not in links:
                    links.append(i.get_attribute('href'))
                    if verbose:
                        print (i.get_attribute('href'), Style.BRIGHT + Fore.GREEN + 'HREF')
            
            for i in img:
                if i.get_attribute('src') not in links:
                    links.append(i.get_attribute('src'))
                    if verbose:
                        print (i.get_attribute('src'), Style.BRIGHT + Fore.GREEN + 'IMAGE')
                    
            for i in script:
                if i.get_attribute('src') not in links:
                    links.append(i.get_attribute('src'))
                    if verbose:
                        print (i.get_attribute('src'), Style.BRIGHT + Fore.GREEN + 'SCRIPT')
                
            pages [current_url] = links
            
        except KeyboardInterrupt:
            break
        except exceptions.StaleElementReferenceException:
            pass
        
    browser.quit()
    #pprint.pprint(pages)
    #pprint.pprint(spiderweb)
    pages = json.dumps(pages)
    
    print (Style.BRIGHT + Fore.GREEN + '[+] Saving the Captured Browsing Info in ' + output_dir + 'spiderweb.json')
    print (Style.BRIGHT + Fore.GREEN + '[+] Saving the Dependency Info in ' + output_dir + 'resources.json')
    
    # Writing the Spider Results into a File
    with open(output_dir + 'spiderweb.json', 'w') as spiderfile:
        json.dump(spiderweb, spiderfile)
        
    with open(output_dir + 'resources.json', 'w') as outfile:
        #pprint.pprint(data, outfile)
        json.dump(pages, outfile)
        
    return pages
        
def parse_urls(base_url, output_dir = '/data'):
    # Opening the Resources File
    print (Style.BRIGHT + Fore.GREEN + '[+] Parsing the Resources Captured in ' + output_dir + 'resources.json')
    with open(output_dir + 'resources.json') as file:
        resources = json.load(file)
        resources = json.loads(resources)
    
    # Initialising Variables  
    results = {}
    external = []
    internal = []
    
    # Parsing the base URL
    base_url = urlparse(base_url)[1]
    #print (base_url)
    
    for page in resources:
        print (Style.BRIGHT + Fore.GREEN + '[+] Parsing Captured URLs for page ' + page)
        for url in resources[page]:
            url_tokens = urlparse(url)
            if url_tokens[1] != base_url:
                external.append(str(url_tokens[1]+url_tokens[2]))
                #print (url_tokens[1], url)
            else:
                internal.append(str(url_tokens[2]))
                
    internal = list(dict.fromkeys(internal))
    external = list(dict.fromkeys(external))
    results['internal'] = internal
    results['external'] = external
    
    print (Style.BRIGHT + Fore.GREEN + '[+] Saving the Parsing Info in ' + output_dir + 'results.json')
    with open(output_dir + 'results.json', 'w') as file:
        json.dump(results, file)


#pages = spider('www.youtube.com')
#parse_urls('https://imgur.com/t/coronavirus')
#pages = spider('https://imgur.com/t/coronavirus')
#pages = spider('http://quotes.toscrape.com/')
