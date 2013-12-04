from gevent import monkey; monkey.patch_all()

from bottle import route, run, request, response, abort
from fight import Fight

@route('/fight')
def fight():
    fight = Fight(request.params.a, request.params.b)
    return fight.get_answer()

run(host='0.0.0.0', port=1234, server='gevent')
