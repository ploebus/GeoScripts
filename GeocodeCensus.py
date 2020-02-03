import requests
import csv



in_file = INFILE
out_file = OUTFILE
BASE_URL = 'https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress'

result_list = []


def getTRACT(lat, lng):
    try:
        resp = requests.get('http://data.fcc.gov/api/block/find?', params={'latitude': lat, 'longitude': lng, 'format': 'json'})
        data = resp.json()
        print(data)
        if data['Block']['FIPS'][5:11]:
            return data['Block']['FIPS'][5:11]
        else: 
            return '99'
    except:
            return '99'





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
                row['F5_LAT'] = data['result']['addressMatches'][0]['coordinates']['y']
                row['F5_LNG'] = data['result']['addressMatches'][0]['coordinates']['x']
                row['F5_TRACT'] = data['result']['addressMatches'][0]['geographies']['2010 Census Blocks'][0]['TRACT']
                row['SOURCE'] = 'CENSUS'
                print("Success: Census")
            else:
                row['F5_LAT'] = '99'
                row['F5_LNG'] = '99'
                row['F5_TRACT'] = '99'
                row['SOURCE'] = 'FAIL'
        except:
            row['F5_LAT'] = '99'
            row['F5_LNG'] = '99'
            row['F5_TRACT'] = '99'
            row['SOURCE'] = 'FAIL'
            print("fail")
        result_list.append(row)


with open(out_file, 'w') as outfile:
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')
    writer.writeheader()
    writer.writerows(result_list)
    print("Done!")
