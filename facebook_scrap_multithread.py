import requests
import json
from pprint import pprint as pp
from multiprocessing.pool import ThreadPool
import time
import matplotlib.pyplot as plt
from functools import reduce
from data import memberData

allMembers = set()
def grab(url):
    member = set()
    feed = requests.get(url).json()['data']
    for eachFeed in feed:        
        member.add(eachFeed['from']['id'])
        if 'comments' in eachFeed:            
            comments = eachFeed['comments']['data']            
            for eachComment in comments:
                member.add(eachComment['from']['id'])
    return member

root = ''
rest = ''
with open('urls.json','r') as infile:
    urls = json.load(infile)
    root = urls['data']['root']
    rest = urls['data']['rest']


#Example algorithm from the root
# pp(grab(root))
plotInfo = []

dead = ThreadPool(processes=100) #wot?
# for eachURL in rest:
#     async_result = dead.apply_async(grab, (eachURL,))    
# start = time.time()
res_list = reduce(lambda setA,setB: setA.union(setB),list(map(lambda eachThread: eachThread.get(),list(map(lambda eachURL: dead.apply_async(grab,(eachURL,)),rest)))))
pp(list(res_list))

# plotInfo.append((i,time.time() - start))    
# pp(time.time() - start)    

# plt.plot( list(map(lambda x:x[0],plotInfo)),list(map(lambda y:y[1],plotInfo)) )
# plt.title('Time needed to retrieve data')
# plt.xlabel('Number of threads')
# plt.ylabel('Time (in second)')
# plt.axis([1, 120, 0, 110])
# plt.show()