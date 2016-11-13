import facebook
import pprint

tokenFile = open("token.txt")

# printi priner
pp = pprint.PrettyPrinter(indent=4)

def getToken(_tokenFile):
    for line in _tokenFile: # change later; just gets the access token from file for privacy
        return line

tokenStr = getToken(tokenFile)

graph = facebook.GraphAPI(access_token=tokenStr, version='2.8')


fb_group = '155607091223285' # utcs fb page
# events = graph.get_object(id=fb_group+ '/feed', fields='from,message_tags,comments{from,message_tags}')

#for fb_element in events["data"]:
    #print("\n\nThis is an element ")
    #pp.pprint(fb_element)
def connect_facebook_user(graph, member_dict):
    '''
    Connect all the users to users who mentioned to each other,
    update the edge based on the feeds fetched from get_object 
    '''

    #Get the feed from the Facebook Graph API
    listOfPosts = graph.get_object(id=fb_group+ '/feed', fields='from,message_tags,message,created_time,comments{from,message_tags}',limit=100)
    # print("These are people")

    # print(member_dict)
    
    for feed in listOfPosts['data']:
        #Get the feed author
        author = feed["from"]["name"]
        
        mentionedHumans = []
        if "message_tags" in feed:
            for humans in feed["message_tags"]:
                if humans["type"] == "user":
                    mentionedHumans.append(humans["name"] )
        # if len(mentionedHumans) != 0:
        #     print("Author")
        #     print(author)
        #     print(mentionedHumans)

        
        if "comments" in feed:       
            for comment in feed["comments"]["data"]:
                #Get the comment author
                author = comment["from"]["name"]
                
                mentionedHumans = []
                if "message_tags" in comment:
                    for humans in comment["message_tags"]:
                        if humans["type"] == "user":
                            mentionedHumans.append(humans["name"] )
                if len(mentionedHumans) != 0:
                    print("comment")
                    print(author)
                    print(mentionedHumans)
        
    '''
    while "next" in listOfPosts["paging"]:
        next_link = listOfPosts["paging"]["next"]
        next_link = next_link.split("/")[-1]
        next_call = fb_group + "/" + next_link
        print(next_call)
        listOfPosts = graph.get_object(next_call,limit=100)

        for feed in listOfPosts['data']:
            #Get the feed author
            author = feed["from"]["name"]
            
            mentionedHumans = []
            
            if "message_tags" in feed:
                for humans in feed["message_tags"]:
                    if humans["type"] == "user":
                        mentionedHumans.append(humans["name"] )
            if len(mentionedHumans) != 0:
                print("Author")
                print(author)
                print(mentionedHumans)
            
            if "comments" in feed:       
                for comment in feed["comments"]["data"]:
                    #Get the comment author
                    author = comment["from"]["name"]
                    
                    mentionedHumans = []
                    
                    
                    if "message_tags" in comment:
                        for humans in feed["message_tags"]:
                            if humans["type"] == "user":
                                mentionedHumans.append(humans["name"] )
                    if len(mentionedHumans) != 0:
                        print("comment")
                        print(author)
                        print(mentionedHumans)
        '''    
        
        
    

    

 

def getMembers(graph):
    membersList = []
    members = graph.get_object(fb_group + "/members",limit=2000,after="")
    


    for user in members["data"]:
        try:
            membersList.append(user["name"])
        except Exception(e):
            print("didn't work")
    
    #Check whether it has more members
    while "next" in members["paging"]:
       after = members["paging"]["cursors"]["after"]
       members = graph.get_object(fb_group + "/members",limit=2000,after=after)

       for user in members["data"]:
        try:
            membersList.append(user["name"])
        except Exception(e):
            print("didn't work")

    print(len(membersList))

    return(membersList)

def getMoreMembers(graph):
    # getMembers(
    pass
# print("The following is a list of the members")
# print(getMembers(graph))

class Node:

    def __init__(self, _name):
        self.name = _name
        self.nodeId = ""
        self.pageRankScore = 0.0
        self.tempPageRankScore = 0.0
        self.edgeOut = []
        self.edgeIn = []


    def addOutgoingRef(self, refName):
        if not isRefExists(edgeOut, refName):
            self.edgeOut.append(refName)

    def addIncomingRef(self, refName):
        if not isRefExists(edgeIn, refName):
            self.edgeIn.append(refName)
    
    def isRefExists(self, edge, refName):
        return refName in edge
    def __str__(self):
        return "My name is name"+ self.name

listOfMembers = {}
# listOfMembers = getMembers(graph) # list of str

memberObjects = {listOfMembers[i]:Node(listOfMembers[i]) for i in range(len(listOfMembers))}
# memberObjects = [Node(listOfMembers[i]) for i in range(len(listOfMembers))]



connect_facebook_user(graph, memberObjects)