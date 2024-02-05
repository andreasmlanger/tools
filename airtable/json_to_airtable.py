"""
Script to synchronize exported JSON from WordPress blog with Airtable
"""

from airtable import Airtable
from dotenv import load_dotenv
import requests
import json
import os
import sys

load_dotenv()

# Airtable
BASE_ID = os.getenv('AIRTABLE_BASE_ID')
TABLE_NAME = os.getenv('AIRTABLE_TABLE_NAME')
TOKEN = os.getenv('AIRTABLE_TOKEN')


def load_json_data():
    """
    Loads exported json data from WordPress blog into dictionary with data & counter as unique key
    """
    with open('data.json', 'r') as f:
        try:
            data = json.load(f)
        except FileNotFoundError:
            sys.exit('Could not find "data.json"!')
    dictionary = {}
    for d in data[::-1]:  # in chronological order
        i = 1
        while True:
            key = f"{d['Date']}-{i}"  # use date with counter as key
            if key not in dictionary:
                break
            i += 1
        dictionary[key] = {'Title': d['Title'], 'Date': d['Date'], 'Tags': d['Tags'], 'Content': d['Content']}
    return dictionary


def update_records_in_airtable():
    """
    Compares data from json and Airtable and updates differing records
    """
    json_data = load_json_data()
    airtable = Airtable(BASE_ID, TABLE_NAME, TOKEN)
    records = airtable.get_all(sort='Date')
    used_keys = set()  # keep track of records with identical date
    for r in records:
        record_id = r['id']
        record_date = r['fields']['Date']
        i = 1
        while True:
            key = f"{record_date}-{i}"
            if key not in used_keys:
                break
            i += 1
        used_keys.add(key)
        flag = False
        for field in ['Title', 'Tags', 'Content']:
            if field not in r['fields']:
                r['fields'][field] = ''
            if r['fields'][field] != json_data[key][field]:
                flag = True
        if flag:
            p = input(f"Differences between JSON\n{json_data[key]}\nand Airtable\n{r['fields']}\nUpdate? (y/n)\n")
            if p == 'y':
                for field in ['Title', 'Tags', 'Content']:
                    r['fields'][field] = json_data[key][field]
                airtable.update(record_id, r['fields'])
                print('Record updated!')

    # Search for new records
    for key in json_data.keys():
        if key not in used_keys:
            fields = json_data[key]
            p = input(f"New record found:\n{fields}\nAdd? (y/n)\n")
            if p == 'y':
                try:
                    airtable.insert(fields)
                except requests.exceptions.HTTPError as ex:
                    sys.exit(str(ex))


update_records_in_airtable()
