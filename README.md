# Running the API
For your convenience, please have virtualenv installed. I'm sure you all have it :)
All the requirements are now in requirements.txt.

- `git clone albert_untung_backend.bundle` or `git clone https://github.com/aulb/api_wrapper_flask`
- `cd albert_untung_backend`
- `virtualenv --no-site-packages -p python3.6 venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- [optional] `deactivate` and `source venv/bin/activate`
- `FLASK_APP=run.py flask run`

You might have to deactivate and reactivate virtualenv. The server should run on localhost:5000 now.

# Design Decisions
There are two major endpoints: /vehicles/:vehicle_id and /vehicles/:vehicle_id/:vehicle_resource. This way the code can be simplified down a little bit.

The decision to use padded JSONIFY is for viewing pleasures only.

# Testing
Run the tests by 
- `cd albert_untung_backend`
- `source venv/bin/activate`
- `python3 tests/test_apis.py`

The tests looks for proper HTTP status codes, proper responses (if 'percent' is float, or if its correctly returning null) and also basic error handling. It should not test values from the thid party's API since we did not build it.

## Common test cases for the APIs:
- Tests for improper HTTP method, i.e using PUT
- Tests for accepted HTTP method but for the wrong resource, i.e GET for /vehicle/:id/engine
- Tests for missing vehicle id, i.e ID: 1123
- Tests for proper request to an endpoint, i.e POST to /vehicle/:id/engine with proper payload

## Fuel/Battery specific tests:
- Tests for gas specific vehicle, should return percent: None for tank level's of battery powered cars
- Tests for electric specific vehicle, vice verse from above

## Engine specific tests:
- Tests for missing payload
- Tests for bad payload (missing 'action' or 'action''s value is not STOP|START)

## General tests:
- Tests for invalid endpoint
