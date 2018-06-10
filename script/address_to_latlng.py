import csv
import requests
import json
print("="*100)
print("start")

address_list = []

f = open('address_utf8.csv','r', encoding='utf-8')
rdr = csv.reader(f)
for line in rdr:
    address_list.append(line)
f.close()

#google geocoding api
api_key = "AIzaSyC_Z3A4Vs3FbqXCvnzqd3S317D-YW8Py-8"

api_url = "https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyC_Z3A4Vs3FbqXCvnzqd3S317D-YW8Py-8&address="

for address in address_list:
    print("주소 : "+api_url+address[3])
    req = requests.get(url=api_url+address[3])
    data = req.json()
    json_str = json.dumps(data)
    json_dict = json.loads(json_str)
    lat = json_dict['results'][0]['geometry']['location']['lat']
    lng = json_dict['results'][0]['geometry']['location']['lng']
    f = open('output.csv', 'a', encoding='utf-8', newline='')
    wr = csv.writer(f)
    wr.writerow([address[0], address[1], address[3],lat,lng])

print("done")
print("="*100)






