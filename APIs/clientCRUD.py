import requests

print('----------------------------POST')
resp0 = requests.post(
    'http://localhost:5000/books/',
    json={
        '1': {
            'author': 'John John',
            'title': 'ARO - masini de epoca',
            'labels': ['auto', 'automobile', 'tehnic']
        },
        '2': {
            'author': 'Tom Tom',
            'title': 'Noapte in munte',
            'labels': ['relief', 'natura']
        },
        '3':{
            'author': 'Steve',
            'title': 'Bucurestiul vechi',
            'labels': ['capitala', 'romania', 'orase']
        }
    }
)
print('status_code is', resp0.status_code)
print('json is', resp0.json())

print('----------------------------')
resp1 = requests.get('http://localhost:5000/books/1/')
print('status_code is', resp1.status_code)
print('json is', resp1.json())####

#prin#t('----------------------------DELETE')
#resp#2 = requests.delete('http://localhost:5000/books/1/')
#prin#t('status_code is', resp2.status_code)
#prin#t('text is', resp2.text)

#print('----------------------------')
#resp3 = requests.get('http://localhost:5000/books/1/')
#print('status_code is', resp3.status_code)
#print('json is', resp3.json())
