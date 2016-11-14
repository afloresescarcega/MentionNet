from flask import Flask,render_template,jsonify

# print a nice greeting.
def say_hello(username = "World"):
    return '<p>Hello %s!</p>\n' % username

# some bits of text for the page.
header_text = '''
    <html>\n<head> <title>EB Flask Test</title> </head>\n<body>'''
instructions = '''
    <p><em>Hint</em>: This is a RESTful web service! Append a username
    to the URL (for example: <code>/Thelonious</code>) to say hello to
    someone specific.</p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'

information = '<p>Facebook Data:</p>'

# EB looks for an 'application' callable by default.
application = Flask(__name__)

# add a rule for the index page.
# application.add_url_rule('/', 'index', (lambda: header_text +
#     say_hello() + instructions + footer_text))

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/data')
def get_data():
    import json
    with open ('facebook_graph.json','r') as f:
        given_dic = (json.load(f))

        #Track down the constructed relationship
        track = set()
        for node in given_dic:
            src_name = given_dic[node]['name']
            targets = given_dic[node]['edgeOut']

            #Construct the list of tuples, to indicate that src is pointing at
            for target in targets:
                track.add((src_name,given_dic[target]['name']))

            #Construct the list of tuples, to indicate that taget is pointing at src
            targets = given_dic[node]['edgeIn']
            for target in targets:
                track.add((given_dic[target]['name'],src_name))

        result_list_dic = []
        for eachRelationship in track:
            result_list_dic.append({'source':eachRelationship[0],'target':eachRelationship[1],"type":"suit"})
        result = {}
        result['data'] = result_list_dic
        #Suppose to return the data for
        # result = {'data':[{'source': "Samsung", 'target': "Apple", "type": "suit"},{'source': "Samsung", 'target': "Apple", "type": "suit"}]}

        return jsonify(result)



# add a rule when the page is accessed with a name appended to the site
# URL.
application.add_url_rule('/<username>', 'hello', (lambda username:
    header_text + say_hello(username) + home_link + footer_text))

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
