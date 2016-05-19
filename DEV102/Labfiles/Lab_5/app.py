import os, uuid, json
from flask import Flask
from flask_restful import Resource, Api, reqparse, abort

weather_url = "http://api.openweathermap.org:80/data/2.5/weather?q=seattle&APPID=b062e1e5bc5d16b03ee57e02964689ed"

app = Flask(__name__)
api = Api(app)


# GET / returns the 2-tier required SG capabilities
@api.resource('/')
class Capability(Resource):
    def get(self):
        return {
            '/services': {
                'POST': {}
            },
            '/services:id': {
                'DELETE': {}
            },
            '/bindings': {
                'POST': {}
            },
            '/bindings/:id': {
                'DELETE': {}
            }
        }


@api.resource('/services')
class Services(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, location='json', required=False, default="A service")
        self.parser.add_argument('description', type=str, location='json', required=False, default="Just another service")
        self.parser.add_argument('params', type=dict, location='json', required=False, default={})
        super(Services, self).__init__()

    def post(self):
        args = self.parser.parse_args()

        resp_json = {}
        resp_json['id'] = str(uuid.uuid4())
        resp_json['name'] = args['name']
        resp_json['description'] = args['description']
        resp_json['params'] = {}

        resp_headers = {}
        resp_headers['X-Service-State'] = json.dumps(args['params'])

        # flask-restful automatically marshals dict-to-json, but not for headers, thus json.* above

        # For this 2-Tier SG, only work is to return url and url_template

        return resp_json, 201, resp_headers


@api.resource('/services/<service_id>')
class Service(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=str, location='json', required=True)
        self.parser.add_argument('force', type=bool, location='json', required=False, default=False)
        self.parser.add_argument('X-Service-State', type=str, location='headers', required=False, default='{}')
        super(Service, self).__init__()

    def delete(self, service_id):
        args = self.parser.parse_args()

        svc = args['id']
        svc = args['force']

        req_headers = {}
        req_headers['X-Service-State'] = json.loads(args['X-Service-State'])

        # No particular work to do in this 2-Tier SG

        return '', 200

@api.resource('/bindings')
class Bindings(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, location='json', required=False, default="service binding")
        self.parser.add_argument('description', type=str, location='json', required=False, default="Just another service binding")
        self.parser.add_argument('service_id', type=str, location='json', required=True)
        self.parser.add_argument('params', type=dict, location='json', required=False, default={})
        self.parser.add_argument('X-Service-State', type=str, location='headers', required=False, default='{}')
        super(Bindings, self).__init__()

    def post(self):
        args = self.parser.parse_args()

        req_headers = {}
        req_headers['X-Service-State'] = json.loads(args['X-Service-State'])

        resp_json = {}
        resp_json['id'] = str(uuid.uuid4())
        resp_json['url'] = weather_url
        resp_json['protocol'] = {'scheme': 'http'}
        resp_json['name'] = args['name']
        resp_json['description'] = args['description']
        resp_json['service_id'] = args['service_id']
        resp_json['params'] = {}

        resp_headers = {}
        resp_headers['X-Binding-State'] = json.dumps(args['params'])

        # flask-restful automatically marshals dict-to-json, but not for headers, thus json.* above

        # For this 2-Tier SG, only work is to return url and url_template

        return resp_json, 201, resp_headers


@api.resource('/bindings/<binding_id>')
class Binding(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=str, location='json', required=True)
        self.parser.add_argument('X-Service-State', type=str, location='headers', required=False, default='{}')
        self.parser.add_argument('X-Binding-State', type=str, location='headers', required=False, default='{}')
        super(Binding, self).__init__()

    def delete(self, binding_id):
        args = self.parser.parse_args()

        binding = args['id']

        req_headers = {}
        req_headers['X-Service-State'] = json.loads(args['X-Service-State'])
        req_headers['X-Binding-State'] = json.loads(args['X-Provider-State'])

        # No particular work to do in this 2-Tier SG

        return '', 200


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    # app.run(debug=True)
