# coding:utf8
"""
Quick utilities and helpers to for the API.
"""
import requests
import json

ENDPOINTS = {
	'fuel': 'http://gmapi.azurewebsites.net/getEnergyService/',
	'doors': 'http://gmapi.azurewebsites.net/getSecurityStatusService/',
	'engine': 'http://gmapi.azurewebsites.net/actionEngineService/',
	'battery': 'http://gmapi.azurewebsites.net/getEnergyService/',
	'vehicles': 'http://gmapi.azurewebsites.net/getVehicleInfoService/'
}
EXCLUDED_LIST = ['twoDoorCoupe']
EXCLUDED_KEYS = dict(zip(EXCLUDED_LIST, [True] * len(EXCLUDED_LIST)))
COMMAND_MAP = {
	'STOP': 'STOP_VEHICLE',
	'START': 'START_VEHICLE'
}
STATUS_MAP = {
	'EXECUTED': 'success',
	'FAILED': 'error'
}
DEFAULT_HEADER = {'Content-Type': 'application/json'}


"""
Validate the response from the initial request to third party API.
"""
def is_successful_request(response):
	return response.status_code == 200 and response.json()['status'] == '200'

def unpack_data(data):
	transformed_data = {}
	for key in data.keys():
		if key not in EXCLUDED_KEYS: 
			transformed_data[key] = apply_type_to_value(data[key])

	return transformed_data

def apply_type_to_value(data):
	# Make sure 'type' is a key in data
	if 'type' not in data: return data

	if data['type'] == 'String':
		return data['value']
	elif data['type'] == 'Boolean':
		return bool(data['value'])
	elif data['type'] == 'Number' or data['type'] == 'Float':
		return float(data['value'])
	elif data['type'] == 'Integer':
		return int(data['value'])
	elif data['type'] == 'Array':
		# Unpack to the bottom
		values = []
		for value in data['values']:
			values.append(unpack_data(value))
		return values
	elif data['type'] == 'Null':
		return None
	return data['value']

def create_payload(vehicle_id, command=None):
	# Default payload
	payload = {
		'id': str(vehicle_id),
		'responseType': 'JSON'
	}
	if command:
		if command in COMMAND_MAP: 
			payload['command'] = COMMAND_MAP[command]
		else: 
			payload['command'] = 'ERROR'

	return payload

def transform_data(request, data):
	if request == 'doors':
		data = data['doors']
	elif request == 'fuel' or request == 'battery':
		fuel_type = 'tankLevel' if request == 'fuel' else 'batteryLevel'
		data = {
			'percent': data[fuel_type]
		}
	elif request == 'engine':
		data['status'] = STATUS_MAP[data['status']]
	return data

"""
Main flow for the API.
"""
def main(request, vehicle_id, action=None):
	# Determine the endpoint we need to hit
	endpoint = ENDPOINTS[request]

	# Create payload with all the necessary parameters given
	command = (request == 'engine' or None) and action
	payload = create_payload(vehicle_id, command=command)

	# Hit the endpoint and validate
	response = requests.post(endpoint, json=payload, headers=DEFAULT_HEADER)
	if not is_successful_request(response): return None

	# Mangle the data
	data_location = 'actionResult' if request == 'engine' else 'data'
	data = unpack_data(response.json()[data_location])
	# Transform the data to the spec provided
	data = transform_data(request, data)
	return data
