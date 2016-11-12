from pprint import pprint
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


def addNode(a):
    if a['name'] not in graph:
        graph[a['name']] = a

def addEdge(a,b):
    '''
    a -> b
    '''
    a['edgeOut'].append(b['name'])
    b['edgeIn'].append(a['name'])


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

class PageRank:
    def __init__(self,graph):
        self.graph = graph
        self.ALPHA = 0.15

    def runPageRank(self):
        s = len(self.graph)
        self.rankSource = self.ALPHA / s

        for page in self.graph:
            self.graph[page]['pageRankScore'] = 1 / s

        '''
        Iteration
        '''
        for i in range(50):
            for eachPage in self.graph:
                incomingScore = 0
                for incomingNode in self.graph[eachPage]['edgeIn']:
                    assert(incomingNode in self.graph)

                    incomingScore += ((self.graph[incomingNode]['pageRankScore']) / len(self.graph[incomingNode]['edgeOut']))
                self.graph[eachPage]['tempPageRankScore'] = (1 - self.ALPHA) * incomingScore + self.rankSource

                c = 1
                tempSum = 0
                for eachPage in self.graph:
                    tempSum += self.graph[eachPage]['tempPageRankScore']
                c /= tempSum

                for eachPage in self.graph:
                    self.graph[eachPage]['pageRankScore'] = c * self.graph[eachPage]['tempPageRankScore']


p = PageRank(graph)
p.runPageRank()
pprint(p.graph)
