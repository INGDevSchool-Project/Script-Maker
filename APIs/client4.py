import requests

print('----------------------------')
resp0 = requests.post(
    'http://localhost:5000/cars/',
    json={
        '1': {
            'car-type': '4 Wheel Drive',
            'brand': 'ARO',
            'color': ['white', 'metal grey', 'blue cosmos', 'army green']
        },
        '2': {
            'car-type': 'sedan',
            'brand': 'saab',
            'color': ['black', 'silver grey', 'blue marin', 'ionic red']
        },
    }
)
print('status_code is', resp0.status_code)
print('json is', resp0.json())

print('----------------------------')
resp1 = requests.get('http://localhost:5000/car/1/')
print('status_code is', resp1.status_code)
print('json is', resp1.json())

print('----------------------------')
resp2 = requests.get('http://localhost:5000/car/2/')
print('status_code is', resp2.status_code)
print('json is', resp2.json())

print('----------------------------')
resp3 = requests.get('http://localhost:5000/car/3/')
print('status_code is', resp3.status_code)
print('json is', resp3.json())