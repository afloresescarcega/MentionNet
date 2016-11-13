'''
The main PageRank algorithm started here
'''

class PageRank:
    def __init__(self,graph):
        '''
        PageRank accepts the graph with the form following:
        graph = {
            'nodeA':nodeA,
            'nodeB':nodeB,
            ...
            'nodeN':nodeN
        }
        '''
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
