"""
    Genie - client

    This is a client which inserts data into the API. This can be used as an initial setup.
    It uses the phenomenal Requests library by Kenneth Reitz.

"""

from csv import DictReader
import json
import requests
from datetime import datetime

ENTRY_POINT = 'localhost:5000'


def post_hosts():
    '''
    uses csv reader to convert csv --> python dictionary --> json then posts into the API
    :return:
    '''
    dict_list = []
    with open('hosts.csv', 'r') as csvfile:
        for d in DictReader(csvfile):
            # convert ports to integer
            d['port'] = int(d['port'])
            dict_list.append(d)

    print('json body: ', json.dumps(dict_list))

    r = perform_post('hosts', json.dumps(dict_list))
    print('posted hosts. HTTP Status: ', r.status_code, r.text)


def post_partnerships():
    '''
    uses an already constructed json string body to do the post.
    :return:
    '''
    json_body = ('['
                 '  {'
                 '    "host": "PSVT-0020",'
                 '    "service": "service1",'
                 '    "action": "action1",'
                 '    "fromPartyId": "fromPartyId",'
                 '    "fromPartyType": "fromPartyType",'
                 '    "fromPartyRole": "fromPartyRole",'
                 '    "toPartyId": "toPartyId",'
                 '    "toPartyType": "toPartyType",'
                 '    "toPartyRole": "toPartyRole",'
                 '    "serviceType": "st",'
                 '    "status": "active"'
                 '  },'
                 '  {'
                 '    "host": "PSVT-0020",'
                 '    "service": "service1",'
                 '    "action": "action2",'
                 '    "fromPartyId": "fromPartyId",'
                 '    "fromPartyType": "fromPartyType",'
                 '    "fromPartyRole": "fromPartyRole",'
                 '    "toPartyId": "toPartyId",'
                 '    "toPartyType": "toPartyType",'
                 '    "toPartyRole": "toPartyRole",'
                 '    "serviceType": "st",'
                 '    "status": "active"'
                 '  },'
                 '  {'
                 '    "host": "PSVT-0020",'
                 '    "service": "service1",'
                 '    "action": "action3",'
                 '    "fromPartyId": "fromPartyId",'
                 '    "fromPartyType": "fromPartyType",'
                 '    "fromPartyRole": "fromPartyRole",'
                 '    "toPartyId": "toPartyId",'
                 '    "toPartyType": "toPartyType",'
                 '    "toPartyRole": "toPartyRole",'
                 '    "serviceType": "st",'
                 '    "status": "active"'
                 '  },'
                 '  {'
                 '    "host": "PSVT-0020",'
                 '    "service": "service1",'
                 '    "action": "action4",'
                 '    "fromPartyId": "fromPartyId",'
                 '    "fromPartyType": "fromPartyType",'
                 '    "fromPartyRole": "fromPartyRole",'
                 '    "toPartyId": "toPartyId",'
                 '    "toPartyType": "toPartyType",'
                 '    "toPartyRole": "toPartyRole",'
                 '    "serviceType": "st",'
                 '    "status": "inactive"'
                 '  },'
                 '  {'
                 '    "host": "NBNTEST03-NBNCO-PSVT-0020",'
                 '    "service": "service2",'
                 '    "action": "action11",'
                 '    "fromPartyId": "fromPartyId",'
                 '    "fromPartyType": "fromPartyType",'
                 '    "fromPartyRole": "fromPartyRole",'
                 '    "toPartyId": "toPartyId",'
                 '    "toPartyType": "toPartyType",'
                 '    "toPartyRole": "toPartyRole",'
                 '    "serviceType": "st",'
                 '    "status": "active"'
                 '  },'
                 '  {'
                 '    "host": "NBNTEST03-NBNCO-PSVT-0020",'
                 '    "service": "service2",'
                 '    "action": "action12",'
                 '    "fromPartyId": "fromPartyId",'
                 '    "fromPartyType": "fromPartyType",'
                 '    "fromPartyRole": "fromPartyRole",'
                 '    "toPartyId": "toPartyId",'
                 '    "toPartyType": "toPartyType",'
                 '    "toPartyRole": "toPartyRole",'
                 '    "serviceType": "st",'
                 '    "status": "active"'
                 '  },'
                 '  {'
                 '    "host": "NBNTEST03-NBNCO-PSVT-0020",'
                 '    "service": "service2",'
                 '    "action": "action13",'
                 '    "fromPartyId": "fromPartyId",'
                 '    "fromPartyType": "fromPartyType",'
                 '    "fromPartyRole": "fromPartyRole",'
                 '    "toPartyId": "toPartyId",'
                 '    "toPartyType": "toPartyType",'
                 '    "toPartyRole": "toPartyRole",'
                 '    "serviceType": "st",'
                 '    "status": "active"'
                 '  }'
                 ']')

    print(json_body)

    r = perform_post('partnerships', json_body)
    print('posted partnerships. HTTP Status: ', r.status_code, r.text)


def perform_post(resource, data):
    headers = {'Content-Type': 'application/json'}
    return requests.post(endpoint(resource), data, headers=headers)


def delete():
    r = perform_delete('people')
    print("'people' deleted", r.status_code)
    r = perform_delete('works')
    print("'works' deleted", r.status_code)


def perform_delete(resource):
    return requests.delete(endpoint(resource))


def endpoint(resource):
    return 'http://{}/{}/'.format(ENTRY_POINT, resource)


if __name__ == "__main__":
    post_hosts()
    post_partnerships()

