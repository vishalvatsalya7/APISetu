import requests
import config
from time import time, sleep

r_state_id = None
r_city_id = None
host_name = 'https://cdn-api.co-vin.in/api'

# headers={'Authorization': 'access_token myToken'}

def get_state_id(state_name):
    api_name_states = '/v2/admin/location/states'
    r_states = requests.get(host_name + api_name_states, headers={'Authorization': 'TOKEN'})
    info = r_states.json()
    list_dict = info['states']
    for dict_ in list_dict:
        if dict_['state_name'] == state_name:
            return dict_['state_id']


def get_city_id(city_name):
    api_name_city = '/v2/admin/location/districts/' + str(r_state_id)
    r_city = requests.get(host_name + api_name_city, headers={'Authorization': 'TOKEN'})
    info = r_city.json()
    list_dict = info['districts']
    for dict_ in list_dict:
        if dict_['district_name'] == city_name:
            return dict_['district_id']


def get_slots(id, date):
    payload = {'district_id': id, 'date': date}
    api_slot = '/v2/appointment/sessions/public/findByDistrict'
    r_slots = requests.get(host_name + api_slot, params=payload, headers={'Authorization': 'TOKEN'})
    return r_slots.json()


def send_message_to_slack(available_capacity, slots, name, min_age_limit):
    from urllib import request, parse
    import json
    post = {"text": "{0} {1} {2} {3}".format(available_capacity, slots, name, min_age_limit)}
    # print(post)
    try:
        json_data = json.dumps(post)
        req = request.Request(config.slack_hook,
                              data=json_data.encode('ascii'),
                              headers={'Content-Type': 'application/json'})
        resp = request.urlopen(req)
    except Exception as em:
        print("EXCEPTION: " + str(em))

def send_notification():
    r_slots = get_slots(r_city_id, '04-05-2021')
    for k, v in r_slots.items():
        for value in v:
            # print(value)
            # if value['min_age_limit'] < 45:
            send_message_to_slack(value['available_capacity'], value['slots'], value['name'],
                                      value['min_age_limit'])


if __name__ == '__main__':
    r_state_id = get_state_id('Uttar Pradesh')
    r_city_id = get_city_id('Mirzapur')
    while True:
        print("sent!")
        send_notification()
        sleep(60 * 60)