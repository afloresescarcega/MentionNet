'''
This script is going to accept the constructed Facebook Graph and return the pageRank for each person in JSON format
'''
from pprint import pprint as pp
from PageRank import PageRank
from facebookHandler import get_Facebook_Graph

def convertGraph():
    '''
    Convert the graph from facebookHandler to the form shown here, for running PageRank
    '''
    result_graph = {}
    fb_graph = get_Facebook_Graph()

    for eachNode in fb_graph:
        edgeOut = []
        edgeIn = []

        edgeOut.extend(fb_graph[eachNode].edgeOut)
        edgeIn.extend(fb_graph[eachNode].edgeIn)


        node = {
            'name': fb_graph[eachNode].name,
            'id': fb_graph[eachNode].name_id,
            'pageRankScore':0.0,
            'tempPageRankScore':0.0,
            'edgeOut': edgeOut,
            'edgeIn': edgeIn
        }

        result_graph[node['id']] = node
    return result_graph

p = PageRank(convertGraph())
p.runPageRank()

import json
with open('facebook_graph.json','w') as fuck:
    json.dump(p.graph,fuck)
    fuck.close()
print("Compete!")
