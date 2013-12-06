from gevent import monkey; monkey.patch_all()

from bottle import route, run, request, response, abort, hook
from twitterfight import TwitterFight
from json import dumps

@route('/fight')
def fight():
    response.content_type = 'application/json'
    fight = TwitterFight(request.params.a, request.params.b)
    return dumps(fight.final_score())

@hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type'

run(host='0.0.0.0', port=1234, server='gevent')
