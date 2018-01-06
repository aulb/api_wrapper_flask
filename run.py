# coding:utf8
from flask import Flask, request
# Jsonpify is padded JSON, for viewing pleasures.
from flask_jsonpify import jsonify
from flask_restplus import Resource, Api
from werkzeug.exceptions import BadRequest
from utils import main
from json import loads

app = Flask(__name__)
api = Api(app)

# Validate the data coming back from the main flow. As of now could only be 'Not found.'
def validate_data(data, message=None):
	if not data: raise BadRequest('Not found.')

@api.route('/vehicles/<int:vehicle_id>')
class VehicleInformation(Resource):
	def get(self, vehicle_id):
		data = main('vehicles', vehicle_id)
		validate_data(data, 'Internal server error.')
		return jsonify(data)
	

@api.route('/vehicles/<int:vehicle_id>/<string:vehicle_resource>')
class VehicleResource(Resource):
	def get(self, vehicle_id, vehicle_resource):
		# Return 404 for GET-ing using inexistent vehicle resource
		if vehicle_resource not in ['doors', 'fuel', 'battery']: raise BadRequest()

		data = main(vehicle_resource, vehicle_id)
		validate_data(data)
		return jsonify(data)

	def post(self, vehicle_id, vehicle_resource):
		if vehicle_resource != 'engine': raise BadRequest()

		if not request.data: raise BadRequest('Payload must not be empty.')
		incoming_payload = loads(request.data)

		# Payload needs to be validated
		action = None if 'action' not in incoming_payload else incoming_payload['action']
		data = main('engine', vehicle_id, action)
		validate_data(data)
		return jsonify(data)


if __name__ == '__main__':
	app.run()
