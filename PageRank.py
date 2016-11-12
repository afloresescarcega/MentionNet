from pprint import pprint
graph = {}

nodeA = {
    'name':'A',
    'id':0,
    'score':0.0,
    'edgeOut':[],
    'edgeIn':[]
}

nodeB = {
    'name':'B',
    'id':1,
    'score':0.0,
    'edgeOut':[],
    'edgeIn':[]
}

def addNode(a):
    if a['name'] not in graph:
        graph[a['name']] = a


def addEdge(a,b):
    '''
    a -> b
    '''
    a['edgeOut'].append(b['name'])
    b['edgeIn'].append(a['name'])

addEdge(nodeA,nodeB)
addNode(nodeA)
addNode(nodeB)
# graph[nodeA['name']] = nodeA
# graph[nodeB['name']] = nodeB
pprint(graph)
