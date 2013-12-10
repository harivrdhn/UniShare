import json
import bottle
from bottle import response, hook, static_file
from json import dumps
from bottle import route, run, request, abort
from pymongo import Connection
 
connection = Connection('localhost', 27017)
db = connection.Test1 

@hook('before_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'

@route('/index')
def index():
    return static_file("display.html",root='html/')

@route('/html/display/:id')
def disp(id):
    return static_file("displayTopic.html", root='html/')

@route('/deletion')
def delete():
    return static_file("delete.html",root='html/')

@route('/topics', method='GET')
def get_topics():
    postarray = []
    results = db['topics'].find()
    for post in results:
        postarray.append(post)
    if not results:
        abort(400, 'No topics with id %s' % id)
    return dumps(postarray)

@route('/topics/:id', method='GET')
def get_topics(id):
    results = db['topics'].find_one({'_id': id})   
    if not results:
        abort(400, 'No topics with id %s' % id)
    return results

#creates a unique topic id --  creates topic 
@route('/topics', method='POST')
def put_topic():
    data = request.body.readline()
    response=[]
    if not data:
	response.append({'response':'No DATA Recieved','responseCode':'400'})
        abort(400, response)
    entity = json.loads(data)
    if not entity.has_key('topicName'):
        response.append({'response':'NO TOPIC NAME PROVIDED','responseCode':'400'})
        abort(400, response)
    if not entity.has_key('author'):
        response.append({'response':'NO AUTHOR NAME PROVIDED','responseCode':'400'})
        abort(400, response)
    if not entity.has_key('desc'):
        entity.desc=""   
    topicId = entity["topicName"]+"_"+entity["author"]
    d = {'_id':topicId, 'desc':entity["desc"], 'topicName': entity["topicName"],'author': entity["author"]}       
       
    try:
	db['topics'].save(d)
	theBody = json.dumps({'topicId': topicId})
        return bottle.HTTPResponse(status=200, body=theBody)       
    except ValidationError as ve:
        abort(400, str(ve))

#update method for updating comments
@route('/topics/<id>/comments', method='POST')
def put_topics(id):
    data = request.body.readline()
    response=[]
    if not data:
	response.append({'response':'No DATA Recieved','responseCode':'400'})
        abort(400, response)        
    entity = json.loads(data)
    if not entity.has_key('author'):
	response.append({'response':'No author specified','responseCode':'400'})
        abort(400, response)
    if not entity.has_key('comment'):
	response.append({'response':'No COMMENT specified','responseCode':'400'})
        abort(400, response)       
    results = db['topics'].find( { '_id': id})   
    if not results:
	response.append({'response':'No Topic Found with id %s' % id,'responseCode':'400'})        
        abort(400, response)
    commentsBuild = []
    commentsBuild.append({'author': entity["author"], 'comment': entity["comment"]})                
        
    for result in results:
        if result.has_key('comments'):
            for commentChild in result["comments"]:
		commentsBuild.append({'author': commentChild["author"], 'comment': commentChild["comment"]})
        d = {'_id':id, 'desc':result["desc"], 'topicName': result["topicName"],'author': result["author"],
         'comments': commentsBuild}      
    	
    	try:
        	db['topics'].save(d)
        	theBody = json.dumps({'Status': "Success",'comments':commentsBuild})
       		return bottle.HTTPResponse(status=200, body=theBody) 
    	except ValidationError as ve:
        	abort(400, str(ve))
    
@route('/topics/:id', method='DELETE')
def delete_topics(id):
    if not id:
	response.append({'response':'No TOPIC ID Recieved','responseCode':'400'})
        abort(400, response) 
    results = db.topics.remove( { '_id': id} )    
    theBody = json.dumps({'Status': "Success"})
    return bottle.HTTPResponse(status=200, body=theBody) 

run(host='localhost', port=8080)
