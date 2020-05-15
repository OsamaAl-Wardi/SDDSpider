import json
from graphviz import Digraph, Graph
from colorama import Style, Fore, init


def spiderweb(output_dir = 'data/', verbose = True):
    dot = Digraph(comment='Spider Web', node_attr={'color': 'lightblue2', 'style': 'filled'})
    dot.attr(size='6,6')
    
    print (Style.BRIGHT + Fore.GREEN + '[+] Reading All Browsing Data from ' + output_dir + 'spiderweb.json')
    with open(output_dir + 'spiderweb.json', 'r') as filehandle:
        basicList = json.load(filehandle)

    pages = list(dict.fromkeys(basicList))# remove duplicates
    
    print (Style.BRIGHT + Fore.GREEN + '[+] Creating Graphs of the Browsing Data from ' + output_dir + 'spiderweb.json')
    for i in range(len(pages)):
        dot.node(str(i),pages[i]) # does not draw duplicate nodes

    # create edges
    for i in range(len(basicList)-1):
        node1 = str(pages.index(basicList[i])) #look up the id of the node
        node2 = str(pages.index(basicList[i+1]))
        dot.edge(node1,node2, label = str(i))
    
    print (Style.BRIGHT + Fore.YELLOW + '[!] Would you like to render the Graph to the Screen? Enter yes/y or no') 
    render = input("")
    if render == 'yes' or render == 'y':
        dot.render(output_dir + 'spiderweb.gv', view=True)
    else:
        dot.render(output_dir + 'spiderweb.gv')

    return dot