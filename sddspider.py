from colorama import Style, Fore, init
import argparse
import time
import os
import spider
import requestor
import grapher
import ripe

intro = '''
      ::::::::  :::::::::  :::::::::          ::::::::  ::::::::: ::::::::::: :::::::::  :::::::::: ::::::::: 
    :+:    :+: :+:    :+: :+:    :+:        :+:    :+: :+:    :+:    :+:     :+:    :+: :+:        :+:    :+: 
   +:+        +:+    +:+ +:+    +:+        +:+        +:+    +:+    +:+     +:+    +:+ +:+        +:+    +:+  
  +#++:++#++ +#+    +:+ +#+    +:+        +#++:++#++ +#++:++#+     +#+     +#+    +:+ +#++:++#   +#++:++#:    
        +#+ +#+    +#+ +#+    +#+               +#+ +#+           +#+     +#+    +#+ +#+        +#+    +#+    
#+#    #+# #+#    #+# #+#    #+#        #+#    #+# #+#           #+#     #+#    #+# #+#        #+#    #+#     
########  #########  #########          ########  ###       ########### #########  ########## ###    ###      

                                        ;               ,           
                                      ,;                 '.         
                                     ;:                   :;        
                                    ::                     ::       
                                    ::                     ::       
                                    ':                     :        
                                     :.                    :        
                                  ;' ::                   ::  '     
                                 .'  ';                   ;'  '.    
                                ::    :;                 ;:    ::   
                                ;      :;.             ,;:     ::   
                                :;      :;:           ,;"      ::   
                                ::.      ':;  ..,.;  ;:'     ,.;:   
                                 "'"...   '::,::::: ;:   .;.;""'    
                                     '"""....;:::::;,;.;"""         
                                 .:::.....'"':::::::'",...;::::;.   
                                ;:' '""'"";.,;:::::;.'""""""  ':;   
                               ::'         ;::;:::;::..         :;  
                              ::         ,;:::::::::::;:..       :: 
                              ;'     ,;;:;::::::::::::::;";..    ':.
                             ::     ;:"  ::::::"""'::::::  ":     ::
                              :.    ::   ::::::;  :::::::   :     ; 
                               ;    ::   :::::::  :::::::   :    ;  
                                '   ::   ::::::....:::::'  ,:   '   
                                 '  ::    :::::::::::::"   ::       
                                    ::     ':::::::::"'    ::       
                                    ':       """""""'      ::       
                                     ::                   ;:        
                                     ':;                 ;:"        
                                       ';              ,;'     Created by: Osama Al-Wardi (The Hijacker)     
                                         "'           '"       Version 1.0
'''

def facilitate_output(path):
  if not os.path.exists(path):
    os.mkdir(path)
    print(Style.BRIGHT + Fore.GREEN + "[+] Directory " + path + " Created")
  else:
    print (Style.BRIGHT + Fore.RED + "[-] Directory " + path + " Already Exists") 
          
def main():
  init(autoreset=True)
  print (Style.BRIGHT + Fore.GREEN + intro)
  time.sleep(0.5)
  parser = argparse.ArgumentParser()
  required = parser.add_argument_group('required arguments')
  required.add_argument("-u", "--url", help="target url including http/https", type=str, required=True)
  parser.add_argument("-o", "--out", help="output directory path", type=str, default='data/')
  parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true", default= False)
  args = parser.parse_args()

  print (args.url)
  facilitate_output(args.out)
  print(Style.BRIGHT + "-------------------- Phase0 - Spidering the Website --------------------")
  spider.spider(args.url, args.out, args.verbose)
  print(Style.BRIGHT + "-------------------- Phase1 - Parsing the Captured URLs --------------------")
  time.sleep(0.5)
  spider.parse_urls(args.url, args.out)
  print(Style.BRIGHT + "-------------------- Phase2 - Capturing All HTTP/HTTPS Requests --------------------")
  time.sleep(0.5)
  requestor.capture_requests(args.out, args.verbose)
  print(Style.BRIGHT + "-------------------- Phase3 - OSINT Anaysis to Gather Perfix and DNS Information --------------------")
  time.sleep(0.5)
  ripe.ripe_lookup(args.url, args.out, args.verbose)
  print(Style.BRIGHT + "-------------------- Phase4 - Visualisation and Graphing --------------------")
  time.sleep(0.5)
  grapher.spiderweb(args.out)
  #grapher.dependency_graph(args.url)

main()