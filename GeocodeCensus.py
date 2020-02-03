import requests
import csv



in_file = INFILE
out_file = OUTFILE
BASE_URL = 'https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress'

result_list = []

with open(in_file, 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')
    n = 1
    for row in reader:
        address = row['ADDRESS_FULL']
        params = {'address': address, 'format': 'json', 'benchmark': '4', 'vintage': '4'}
        print(row)
        try:
            resp = requests.get(BASE_URL, params=params, headers={"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'})
            data = resp.json()
            print(data['result']['addressMatches'][0]['geographies']['2010 Census Blocks'][0]['TRACT'])
            print("Length: ",len(data['result']['addressMatches']))
            if len(data['result']['addressMatches']) > 0:
                row['lat'] = data['result']['addressMatches'][0]['coordinates']['y']
                row['lng'] = data['result']['addressMatches'][0]['coordinates']['x']
                row['tract'] = data['result']['addressMatches'][0]['geographies']['2010 Census Blocks'][0]['TRACT']
                row['source'] = 'CENSUS'
                print("Success: Census")
            else:
                row['lat'] = '99'
                row['lng'] = '99'
                row['tract'] = '99'
                row['source'] = 'FAIL'
        except:
            row['lat'] = '99'
            row['lng'] = '99'
            row['tract'] = '99'
            row['source'] = 'FAIL'
            print("fail")
        result_list.append(row)


with open(out_file, 'w') as outfile:
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')
    writer.writeheader()
    writer.writerows(result_list)
    print("Done!")
