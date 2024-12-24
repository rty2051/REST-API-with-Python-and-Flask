from flask import Flask, url_for
from flask import request
from flask import json
from flask import Response
from functools import wraps
from flask import jsonify



app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/articles')
def api_articles():
    return 'List of ' + url_for('api_articles')

@app.route('/articles/<articleid>')
def api_article(articleid):
    return 'You are reading ' + articleid

# @app.route('/hello')
# def api_hello():
#     if 'name' in request.args:
#         return 'Hello ' + request.args['name']
#     else:
#         return 'Hello John Doe'

@app.route('/echo', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():
    if request.method == 'GET':
        return "ECHO: GET\n"
    elif request.method == 'POST':
        return "ECHO: POST\n"
    elif request.method == 'PATCH':
        return "ECHO: PATCH\n"
    elif request.method == 'PUT':
        return "ECHO: PUT\n"
    elif request.method == 'DELETE':
        return "ECHO: DELETE\n"


@app.route('/messages', methods = ['POST'])
def api_message():
    if request.headers['Content-Type'] == 'text/plain':
        return "Text Message: " + request.data
    elif request.headers['Content-Type'] == 'application/json':
        return "JSON Message: " + json.dumps(request.json)
    elif request.headers['Content-Type'] == 'application/octet-stream':
        f = open('./binary', 'wb')
        f.write(request.data)
        f.close()
        return "Binary message written!"
    else:
        return "415 Unsupported Media Type ;)"
    
# @app.route('/hello', methods = ['GET'])
# def api_hello():
#     data = {
#         'hello'   :   'world',
#         'number'  :   3
#     }
#     js = json.dumps(data)

#     # resp = Response(js, status=200, mimetype='application/json')
#     resp = jsonify(data)
#     resp.status_code = 200
#     resp.headers['Link'] = 'http://luisrei.com'

#     return resp

@app.errorhandler(404)
def not_found(error=None):
    message={
        'status': 404,
        'message': 'Not Found: ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.route('/users/<userid>', methods=['GET'])
def api_users(userid):
    users = {'1':'john', '2':'steve','3':'bill'}
    if userid in users:
        return jsonify({userid:users[userid]})
    else:
        return not_found()

def check_auth(username, password):
    return username == 'admin' and password == 'secret'

def authenticate():
    message = {'message': 'Authenticate.'}
    resp = jsonify(message)

    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'

    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()
        elif not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# @app.route('/secrets')
# @requires_auth
# def api_hello():
#     return "Shhh this is top secret spy stuff!"

@app.route('/hello', methods = ['GET'])
def api_hello():
    app.logger.info('informing')
    app.logger.warning('warning')
    app.logger.error('screaming bloody murder!')
    return "check your logs\n"

if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
    import logging
    file_handler = logging.FileHandler('app.log')
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)