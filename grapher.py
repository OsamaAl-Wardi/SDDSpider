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
    #print (pages)
    # create nodes
    
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

def dependency_graph(base_url):
    g = Digraph('G', engine='fdp', node_attr={'color': 'lightblue2', 'style': 'filled'})
    g.attr(label=base_url)
    g.attr(fontsize='20')
    with g.subgraph(name='clusterT') as t:
        #t.node('Bootstrap')
        #t.node('Googlefonts')
        t.node('TLS v1.0 Ciphers')
        t.node('Go Daddy Certificate Authority')
        t.attr(label='Web Application')
        with t.subgraph(name='clusterA') as a:
            a.attr(label='Client Side')
            #a.node('other internal pages')
            
            with open('data/results.json', 'r') as file:
                results = json.load(file)
            
            for dependency in results['internal']:
                a.node(dependency)
            
            
        with t.subgraph(name='clusterB') as b:
            b.node('nginx')
            b.node('ubuntu')
            b.attr(label='Server Side')

        #t.edge('clusterA', 'Bootstrap')
        #t.edge('clusterA', 'Googlefonts')
        for dependency in results['external']:
            t.edge(dependency.replace(':', ''), 'clusterA')
        t.edge('TLS v1.0 Ciphers', 'clusterB')
        t.edge('Go Daddy Certificate Authority', 'clusterB')

    g.render('output/test.gv', view=True)
    
#dependency_graph('http://quotes.toscrape.com/')
#dependency_graph('https://www.youtube.com/watch?v=kGXvP1RRLKw')
#spiderweb()