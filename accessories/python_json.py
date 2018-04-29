import json

book = {}
book["victor"] = {
    'name': 'Victor Ughonu',
    'address': '6 Kayode Ogbomosho street Ipaja-Ayobo',
    'phone': '08165660498'
}

book["miracle"] = {
    'name': 'miracle Ughonu',
    'address': '6 Kayode Ogbomosho street Ipaja-Ayobo',
    'phone': '08066998250'
}

s = json.dumps(book)
print(s)