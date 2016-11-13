'''
A script that demonstrate running PageRank algorithm with the given graph
'''

from pprint import pprint as pp
from PageRank import PageRank

def constructGraph():
    def addNode(a):
        if a['id'] not in graph:
            graph[a['id']] = a

    def addEdge(a,b):
        '''
        a -> b
        '''
        a['edgeOut'].append(b['id'])
        b['edgeIn'].append(a['id'])

    graph = {}

    nodeA = {
        'name':'A',
        'id':0,
        'pageRankScore':0.0,
        'tempPageRankScore':0.0,
        'edgeOut':[],
        'edgeIn':[]
    }
    nodeB = {
        'name':'B',
        'id':1,
        'pageRankScore':0.0,
        'tempPageRankScore':0.0,
        'edgeOut':[],
        'edgeIn':[]
    }
    nodeC = {
        'name':'C',
        'id':2,
        'pageRankScore':0.0,
        'tempPageRankScore':0.0,
        'edgeOut':[],
        'edgeIn':[]
    }
    nodeD = {
        'name':'D',
        'id':3,
        'pageRankScore':0.0,
        'tempPageRankScore':0.0,
        'edgeOut':[],
        'edgeIn':[]
    }
    nodeE = {
        'name':'E',
        'id':4,
        'pageRankScore':0.0,
        'tempPageRankScore':0.0,
        'edgeOut':[],
        'edgeIn':[]
    }

    addNode(nodeA)
    addNode(nodeB)
    addNode(nodeC)
    addNode(nodeD)
    addNode(nodeE)

    addEdge(nodeA,nodeB)
    addEdge(nodeA,nodeC)

    addEdge(nodeB,nodeC)
    addEdge(nodeB,nodeD)

    addEdge(nodeC,nodeA)
    addEdge(nodeC,nodeE)

    addEdge(nodeE,nodeC)

    return graph
    
p = PageRank(constructGraph())
p.runPageRank()
pp(p.graph)
