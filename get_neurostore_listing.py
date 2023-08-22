import requests
import json

url= "https://neurostore.xyz/api/base-studies/?page_size=29999&flat=true"

response = requests.get(url)
data = response.json()
with open('neurostore_listing.json', 'w') as outfile:
    json.dump(data, outfile, indent=4, sort_keys=True)

