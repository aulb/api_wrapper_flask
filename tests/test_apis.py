# coding:utf8
import unittest
import requests
import json

BASE_URL = 'http://localhost:5000'
NOT_FOUND = {'message': 'Not found.'}
NOT_ALLOWED_HTTP = {'message': 'The method is not allowed for the requested URL.'}
WRONG_HTTP = {'message': 'The browser (or proxy) sent a request that this server could not understand.'}
EMPTY_PAYLOAD = {"message": "Payload must not be empty."}
# The two valid vehicles we are supplied with.
VALID_GAS_ID = '1234'
VALID_ELECTRIC_ID = '1235'
# For test vehicles that we know are not there.
INVALID_ID = '1123'

class TestVehiclesEndpoint(unittest.TestCase):
	# Camelcase vs underscore => Flask implements things in camelcase
	def setUp(self):
		self.create_endpoint = lambda vehicle_id: '{}/vehicles/{}'.format(BASE_URL, vehicle_id)

	def test_improper_http_method(self):
		response = requests.post(self.create_endpoint(VALID_GAS_ID))
		# Test for proper response status
		self.assertEqual(response.status_code, 405)
		self.assertEqual(response.json(), NOT_ALLOWED_HTTP)

	def test_invalid_vehicle_id(self):
		response = requests.get(self.create_endpoint(INVALID_ID))
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json(), NOT_FOUND)

	def test_proper_request(self):
		expected_response = {
			'color': 'Metallic Silver', 
			'driveTrain': 'v8', 
			'fourDoorSedan': True, 
			'vin': '123123412412'
		}
		response = requests.get(self.create_endpoint(VALID_GAS_ID))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json(), expected_response)


class TestSecurityEndpoint(unittest.TestCase):
	def setUp(self):
		self.create_endpoint = lambda vehicle_id: '{}/vehicles/{}/doors'.format(BASE_URL, vehicle_id)

	# Test for put or head for example
	def test_improper_http_method(self):
		response = requests.put(self.create_endpoint(VALID_GAS_ID))
		# Test for proper response status
		self.assertEqual(response.status_code, 405)
		self.assertEqual(response.json(), NOT_ALLOWED_HTTP)

	# Test for post specifically
	def test_accepted_http_method_wrong_resource(self):
		response = requests.post(self.create_endpoint(VALID_GAS_ID))
		# Test for proper response status
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json(), WRONG_HTTP)

	def test_invalid_vehicle_id(self):
		response = requests.get(self.create_endpoint(INVALID_ID))
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json(), NOT_FOUND)

	def test_proper_request(self):
		expected_response = [
			{'locked': True, 'location': 'frontLeft'},
			{'locked': True, 'location': 'frontRight'} 
		]
		response = requests.get(self.create_endpoint(VALID_ELECTRIC_ID))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json(), expected_response)


class TestFuelEndpoint(unittest.TestCase):
	def setUp(self):
		self.create_endpoint = lambda vehicle_id: '{}/vehicles/{}/fuel'.format(BASE_URL, vehicle_id)

	def test_improper_http_method(self):
		response = requests.put(self.create_endpoint(VALID_GAS_ID))
		# Test for proper response status
		self.assertEqual(response.status_code, 405)
		self.assertEqual(response.json(), NOT_ALLOWED_HTTP)

	def test_accepted_http_method_wrong_resource(self):
		response = requests.post(self.create_endpoint(VALID_GAS_ID))
		# Test for proper response status
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json(), WRONG_HTTP)

	def test_invalid_vehicle_id(self):
		response = requests.get(self.create_endpoint(INVALID_ID))
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json(), NOT_FOUND)

	def test_gas_vehicle(self):
		response = requests.get(self.create_endpoint(VALID_GAS_ID))
		self.assertEqual(response.status_code, 200)
		# TODO: Could use json schema validation here!
		assert('percent' in response.json())
		self.assertEqual(type(response.json()['percent']), float)

	def test_electric_vehicle(self):
		response = requests.get(self.create_endpoint(VALID_ELECTRIC_ID))
		self.assertEqual(response.status_code, 200)
		assert('percent' in response.json())
		self.assertEqual(response.json()['percent'], None)

"""
Identical test to fuel endpoint.
"""
class TestBatteryEndpoint(unittest.TestCase):
	def setUp(self):
		self.create_endpoint = lambda vehicle_id: '{}/vehicles/{}/battery'.format(BASE_URL, vehicle_id)

	def test_improper_http_method(self):
		response = requests.put(self.create_endpoint(VALID_GAS_ID))
		# Test for proper response status
		self.assertEqual(response.status_code, 405)
		self.assertEqual(response.json(), NOT_ALLOWED_HTTP)

	def test_accepted_http_method_wrong_resource(self):
		response = requests.post(self.create_endpoint(VALID_GAS_ID))
		# Test for proper response status
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json(), WRONG_HTTP)

	def test_invalid_vehicle_id(self):
		response = requests.get(self.create_endpoint(INVALID_ID))
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json(), NOT_FOUND)

	def test_gas_vehicle(self):
		response = requests.get(self.create_endpoint(VALID_GAS_ID))
		self.assertEqual(response.status_code, 200)
		assert('percent' in response.json())
		self.assertEqual(response.json()['percent'], None)

	def test_electric_vehicle(self):
		response = requests.get(self.create_endpoint(VALID_ELECTRIC_ID))
		self.assertEqual(response.status_code, 200)
		assert('percent' in response.json())
		self.assertEqual(type(response.json()['percent']), float)


class TestEngineEndpoint(unittest.TestCase):
	def setUp(self):
		self.create_endpoint = lambda vehicle_id: '{}/vehicles/{}/engine'.format(BASE_URL, vehicle_id)
		self.create_payload = lambda action: {'action': action}

	def test_improper_http_method(self):
		dummy_payload = self.create_payload('START')
		response = requests.put(self.create_endpoint(VALID_GAS_ID), json=dummy_payload)
		# Test for proper response status
		self.assertEqual(response.status_code, 405)
		self.assertEqual(response.json(), NOT_ALLOWED_HTTP)

	def test_accepted_http_method_wrong_resource(self):
		response = requests.get(self.create_endpoint(VALID_GAS_ID))
		# Test for proper response status
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json(), WRONG_HTTP)

	def test_invalid_vehicle_id(self):
		dummy_payload = self.create_payload('START')
		response = requests.post(self.create_endpoint(INVALID_ID), json=dummy_payload)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json(), NOT_FOUND)

	def test_missing_payload(self):
		response = requests.post(self.create_endpoint(VALID_GAS_ID))
		# TODO: clarify best practice for validating payloads
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json(), EMPTY_PAYLOAD)

	def test_bad_payload(self):
		dummy_payload = self.create_payload('HALT')
		response = requests.post(self.create_endpoint(VALID_GAS_ID), json=dummy_payload)
		self.assertEqual(response.status_code, 400)
		# TODO: clarify best practice for validating payloads and returns
		self.assertEqual(response.json(), NOT_FOUND)

	def test_proper_request(self):
		dummy_payload = self.create_payload('START')
		response = requests.post(self.create_endpoint(VALID_GAS_ID), json=dummy_payload)
		self.assertEqual(response.status_code, 200)
		assert('status' in response.json() and response.json()['status'] in ['success', 'error'])

		dummy_payload = self.create_payload('STOP')
		response = requests.post(self.create_endpoint(VALID_GAS_ID), json=dummy_payload)
		self.assertEqual(response.status_code, 200)
		assert('status' in response.json() and response.json()['status'] in ['success', 'error'])

"""
Test for non existant endpoints.
"""
class TestGeneralEndpoint(unittest.TestCase):
	def test_invalid_endpoint(self):
		response = requests.get('{}/nonexistant/'.format(BASE_URL))
		self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
	unittest.main()
