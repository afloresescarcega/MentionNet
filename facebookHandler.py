import facebook
from pprint import pprint as pp

def getToken(_tokenFile):
    for line in _tokenFile: # change later; just gets the access token from file for privacy
        return line
tokenFile = open("token.txt")

tokenStr = getToken(tokenFile)

class Node:
    def __init__(self, name_id,name):
        self.name = name
        self.name_id = name_id
        self.pageRankScore = 0.0
        self.tempPageRankScore = 0.0
        self.edgeOut = set()
        self.edgeIn = set()

    def add_edge_out(self, ref_id):
        self.edgeOut.add(ref_id)

    def add_edge_in(self, ref_id):
        self.edgeIn.add(ref_id)

    def __str__(self):
        return "My name is name"+ self.name

Facebook_Graph_API = facebook.GraphAPI(access_token=tokenStr, version='2.8')


# UTCS Facebook page ID
fb_group = '155607091223285'

#This method only process the feed
def scrap_facebook_user_mention_helper(feed,member_dict):
    '''
    dfs
    '''
    for feed in feed["data"]:        
        author_name,author_id = feed["from"]["name"], feed["from"]["id"]    

        if author_id not in member_dict:
            member_dict[author_id] = Node(author_id,author_name)    

        if "message_tags" in feed:            
            mentionedHumans = [(humans["id"],humans["name"]) for humans in feed["message_tags"] if "type" in humans and humans["type"] == "user"]            
            for mentioned_human in mentionedHumans:
                if mentioned_human[0] not in member_dict:
                    member_dict[mentioned_human[0]] = Node(mentioned_human[0],mentioned_human[1])
                #Everyone of the humans who mentioned by the author will be recorded in the edgeIn
                member_dict[mentioned_human[0]].add_edge_in(author_id)

                #Everyone of the humans whom the author mentioned will be recorded in the edgeOut
                member_dict[author_id].add_edge_out(mentioned_human[0])

        if "comments" in feed:
            scrap_facebook_user_mention_helper(feed["comments"],member_dict)


#This method only process whether the given feed has paging or not
def scrap_facebook_user_mention(Facebook_Graph_API,limit,limit2=150):    
    member_dict = {}

    #Get the feed from the Facebook Graph API
    feeds = Facebook_Graph_API.get_object(id=fb_group+ '/feed', fields='from,message_tags,message,created_time,comments{from,message_tags,comments{from,message_tags}}',limit=limit)
    scrap_facebook_user_mention_helper(feeds,member_dict)

    while "paging" in feeds:        
        next_call = fb_group + "/" + feeds["paging"]["next"].split("/")[-1]        
        feeds = Facebook_Graph_API.get_object(next_call,limit=limit2)
        scrap_facebook_user_mention_helper(feeds,member_dict)

    return {k:v for k,v in member_dict.items() if len(v.edgeIn) > 0 or len(v.edgeOut) > 0}        

a = scrap_facebook_user_mention(Facebook_Graph_API,30,30)
# b = scrap_facebook_user_mention(Facebook_Graph_API,40,40)
# diff_set = (set(a) ^ set(b))
# for i in diff_set:
#     pp(i)
#     if i not in a:
#         pp(b[i].edgeOut)
#     else:
#         pp(a[i].edgeOut)


def connect_facebook_user(Facebook_Graph_API):
    '''
    Construct the Facebook network graph in the UTCS group
    '''
    member_dict = {}

    #Get the feed from the Facebook Graph API
    feeds = Facebook_Graph_API.get_object(id=fb_group+ '/feed', fields='from,message_tags,message,created_time,comments{from,message_tags,comments{from,message_tags}}',limit=150)

    for feed in feeds['data']:
        #Get the feed author_name
        author_name = feed["from"]["name"]
        author_id = feed["from"]["id"]

        #Keep getting new members in the member_dict if they haven't existed in the dictionary yet
        if author_id not in member_dict:
            member_dict[author_id] = Node(author_id,author_name)

        mentionedHumans = []
        if "message_tags" in feed:
            '''
            Prepare to construct outlinks from the given author
            '''
            for humans in feed["message_tags"]:
                if humans["type"] == "user":
                    mentionedHumans.append((humans["id"],humans["name"]))

            # if len(mentionedHumans) != 0:
            #     print("author_name")
            #     print(author_name + ": " + author_id)
            #     print(author_name + " had mentioned")
            #     print(mentionedHumans)

        #Insert the mentioned humans from the feed author to the member dict
        for mentioned_human in mentionedHumans:
            if mentioned_human[0] not in member_dict:
                member_dict[mentioned_human[0]] = Node(mentioned_human[0],mentioned_human[1])

            #Everyone of the humans who mentioned by the author will be recorded in the edgeIn
            member_dict[mentioned_human[0]].add_edge_in(author_id)

            #Everyone of the humans whom the author mentioned will be recorded in the edgeOut
            member_dict[author_id].add_edge_out(mentioned_human[0])

        '''
        Only deal with mentioning on layer of the comment for each feed
        '''
        if "comments" in feed:
            for comment in feed["comments"]["data"]:
                #Get the comment author_name
                #Warning: Each of the comment is authorzied by differnt user
                author_name = comment["from"]["name"]
                author_id = comment["from"]["id"]

                #Keep getting new members in the member_dict if they haven't existed in the dictionary yet
                if author_id not in member_dict:
                    member_dict[author_id] = Node(author_id,author_name)

                '''
                Just like what we did in feed, but instead for comments
                '''
                mentionedHumans = []
                if "message_tags" in comment:
                    for humans in comment["message_tags"]:
                        if humans["type"] == "user":
                            mentionedHumans.append((humans["id"],humans["name"]))

                # if len(mentionedHumans) != 0:
                #     print("comment")
                #     print(author_name + ": " + author_id)
                #     print(mentionedHumans)

                #Insert the mentioned humans from the feed author to the member dict
                for mentioned_human in mentionedHumans:
                    if mentioned_human[0] not in member_dict:
                        member_dict[mentioned_human[0]] = Node(mentioned_human[0],mentioned_human[1])

                    #Everyone of the humans who mentioned by the author will be recorded in the edgeIn
                    member_dict[mentioned_human[0]].add_edge_in(author_id)

                    #Everyone of the humans whom the author mentioned will be recorded in the edgeOut
                    member_dict[author_id].add_edge_out(mentioned_human[0])

                    if "comments" in comment:
                        for sub_comment in comment["comments"]["data"]:
                            #Get the comment author_name
                            #Warning: Each of the comment is authorzied by differnt user
                            author_name = sub_comment["from"]["name"]
                            author_id = sub_comment["from"]["id"]

                            #Keep getting new members in the member_dict if they haven't existed in the dictionary yet
                            if author_id not in member_dict:
                                member_dict[author_id] = Node(author_id,author_name)

                            '''
                            Just like what we did in feed, but instead for comments
                            '''
                            mentionedHumans = []
                            if "message_tags" in sub_comment:
                                for humans in sub_comment["message_tags"]:
                                    if humans["type"] == "user":
                                        mentionedHumans.append((humans["id"],humans["name"]))

                            # if len(mentionedHumans) != 0:
                            #     print("comment")
                            #     print(author_name + ": " + author_id)
                            #     print(mentionedHumans)

                            #Insert the mentioned humans from the feed author to the member dict
                            for mentioned_human in mentionedHumans:
                                if mentioned_human[0] not in member_dict:
                                    member_dict[mentioned_human[0]] = Node(mentioned_human[0],mentioned_human[1])

                                #Everyone of the humans who mentioned by the author will be recorded in the edgeIn
                                member_dict[mentioned_human[0]].add_edge_in(author_id)

                                #Everyone of the humans whom the author mentioned will be recorded in the edgeOut
                                member_dict[author_id].add_edge_out(mentioned_human[0])



    while "paging" in feeds:
        next_link = feeds["paging"]["next"]
        next_link = next_link.split("/")[-1]
        next_call = fb_group + "/" + next_link
        feeds = Facebook_Graph_API.get_object(next_call,limit=150)

        for feed in feeds['data']:
            #Get the feed author_name
            author_name = feed["from"]["name"]
            author_id = feed["from"]["id"]

            #Keep getting new members in the member_dict if they haven't existed in the dictionary yet
            if author_id not in member_dict:
                member_dict[author_id] = Node(author_id,author_name)

            mentionedHumans = []
            if "message_tags" in feed:
                '''
                Prepare to construct outlinks from the given author
                '''
                for humans in feed["message_tags"]:
                    if humans["type"] == "user":
                        mentionedHumans.append((humans["id"],humans["name"]))

                # if len(mentionedHumans) != 0:
                #     print("author_name")
                #     print(author_name + ": " + author_id)
                #     print(author_name + " had mentioned")
                #     print(mentionedHumans)

            #Insert the mentioned humans from the feed author to the member dict
            for mentioned_human in mentionedHumans:
                if mentioned_human[0] not in member_dict:
                    member_dict[mentioned_human[0]] = Node(mentioned_human[0],mentioned_human[1])

                #Everyone of the humans who mentioned by the author will be recorded in the edgeIn
                member_dict[mentioned_human[0]].add_edge_in(author_id)

                #Everyone of the humans whom the author mentioned will be recorded in the edgeOut
                member_dict[author_id].add_edge_out(mentioned_human[0])

            '''
            Only deal with mentioning on layer of the comment for each feed
            '''
            if "comments" in feed:
                for comment in feed["comments"]["data"]:
                    #Get the comment author_name
                    #Warning: Each of the comment is authorzied by differnt user
                    author_name = comment["from"]["name"]
                    author_id = comment["from"]["id"]

                    #Keep getting new members in the member_dict if they haven't existed in the dictionary yet
                    if author_id not in member_dict:
                        member_dict[author_id] = Node(author_id,author_name)

                    '''
                    Just like what we did in feed, but instead for comments
                    '''
                    mentionedHumans = []
                    if "message_tags" in comment:
                        for humans in comment["message_tags"]:
                            try:
                                if humans["type"] == "user":
                                    mentionedHumans.append((humans["id"],humans["name"]))
                            except KeyError:
                                pp("Facebook has an error on one of the data we don't care for now")

                    # if len(mentionedHumans) != 0:
                    #     print("comment")
                    #     print(author_name + ": " + author_id)
                    #     print(mentionedHumans)

                    #Insert the mentioned humans from the feed author to the member dict
                    for mentioned_human in mentionedHumans:
                        if mentioned_human[0] not in member_dict:
                            member_dict[mentioned_human[0]] = Node(mentioned_human[0],mentioned_human[1])

                        #Everyone of the humans who mentioned by the author will be recorded in the edgeIn
                        member_dict[mentioned_human[0]].add_edge_in(author_id)

                        #Everyone of the humans whom the author mentioned will be recorded in the edgeOut
                        member_dict[author_id].add_edge_out(mentioned_human[0])

                    if "comments" in comment:
                        for sub_comment in comment["comments"]["data"]:
                            #Get the comment author_name
                            #Warning: Each of the comment is authorzied by differnt user
                            author_name = sub_comment["from"]["name"]
                            author_id = sub_comment["from"]["id"]

                            #Keep getting new members in the member_dict if they haven't existed in the dictionary yet
                            if author_id not in member_dict:
                                member_dict[author_id] = Node(author_id,author_name)

                            '''
                            Just like what we did in feed, but instead for comments
                            '''
                            mentionedHumans = []
                            if "message_tags" in sub_comment:
                                for humans in sub_comment["message_tags"]:
                                    if humans["type"] == "user":
                                        mentionedHumans.append((humans["id"],humans["name"]))

    # for node in member_dict:
    #     if len(member_dict[node].edgeIn) > 1 or len(member_dict[node].edgeIn) > 1:
    #         pp("-----------------")
    #         pp(member_dict[node].name)
    #         pp("edgeOut")
    #         pp(member_dict[node].edgeOut)
    #         pp("edgeIn")
    #         pp(member_dict[node].edgeIn)
    #         pp("-----------------")
    #         print()
    #     # pp(member_dict[node].name)
    # pp(len(member_dict))
    return {k:v for k,v in member_dict.items() if len(v.edgeIn) > 0 or len(v.edgeOut) > 0}



def get_Facebook_Graph():
    return scrap_facebook_user_mention(Facebook_Graph_API)


def getMembers(Facebook_Graph_API):
    membersList = []
    members = Facebook_Graph_API.get_object(fb_group + "/members",limit=2000,after="")



    for user in members["data"]:
        try:
            membersList.append(user["name"])
        except Exception(e):
            print("didn't work")

    #Check whether it has more members
    while "next" in members["paging"]:
       after = members["paging"]["cursors"]["after"]
       members = Facebook_Graph_API.get_object(fb_group + "/members",limit=2000,after=after)

       for user in members["data"]:
        try:
            membersList.append(user["name"])
        except Exception(e):
            print("didn't work")

    return(membersList)
