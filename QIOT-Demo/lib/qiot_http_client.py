#!/usr/bin/env python
import requests
import json
import os
from datetime import datetime


class QIOT:
    def __init__(self, config_file):

        self.config_file = config_file
        self.config = self.get_config()

        self.host_url = self.config["host_url"]
        self.account_token = self.config["account_token"]
        self.api_token = self.config["api_token"]

        self.label = self.config["label"]
        self.identity = self.config["identity"]

        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'QIOT ' + self.account_token
        }
        self.json = {}
        self.collection_token = None
        self.thing_token = None

    def register(self, label, identity):
        if label:
            self.label = label
        if identity:
            self.identity = identity

        registration_json = {'label': self.label, 'identity': self.identity}

        if self.collection_token != {}:
            registration_json = {'label': self.label, 'identity': self.identity,  'collection_token': self.collection_token}

        r = requests.post(url=self.host_url + '/1/r', headers=self.headers, json=registration_json)

        if r.status_code == 200:
            current_timestamp = (datetime.now()).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            print(current_timestamp, '=> Registration accepted!', r.status_code)
            with open("qiot-keys-" + self.identity[0]["value"] + ".json", "w") as outfile:
                outfile.write(r.text)
            return json.loads(r.text)

    def publish_message_to_thing(self, message, thing_token):
        if (message is None) or (message == {}) or (message == []) or (message == [{}]) or (message == [None]):
            return
        message_format = {"messages": message}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'QIOT ' + self.account_token
        }
        url = self.host_url + '/1/l/' + thing_token

        r = requests.post(url=url, headers=headers, json=message_format)

        current_timestamp = (datetime.now()).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        if r.status_code == 200 or r.status_code == 204:
            print(current_timestamp, '=> Message published with status code ' + str(r.status_code) +  ' to : ', url, json.dumps(message_format) )
        else:
            print(current_timestamp, "=> Something went wrong, the status code was:", r.status_code, r.text)

    def get_messages_from_thing(self, thing_token, binaries_limit, limit, start_time, end_time):

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.api_token
        }

        url = 'https://qiot.io' + '/messages/messages?thing_token=' + thing_token + '&binaries_limit=' + str(binaries_limit) + '&limit=' + str(limit) + \
              '&time_from=' + start_time + '&time_end=' + end_time

        r = requests.get(url=url, headers=headers)
        print("the status code was:", r.status_code)
        if r.status_code == 200:
            return json.loads(r.text)
        pass

    def subscribe_to_thing(self, thing_token):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'QIOT ' + self.account_token
        }
        url = self.host_url + '/1/l/' + thing_token
        r = requests.get(url=url, headers=headers)
        print(r.status_code)

        if r.status_code == 200:
            return json.loads(r.text)

    def listen_to_mailbox(self, thing_token):
        # Listening events wont work well with http. Need a mqtt client
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'QIOT ' + self.account_token
        }
        url = self.host_url + '/1/m/' + thing_token
        r = requests.get(url=url, headers=headers)
        print(r.status_code)

        if r.status_code == 200:
            return json.loads(r.text)

    def listen_to_collection(self, collection_token):
        # Listening events wont work well with http. Need a mqtt client
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'QIOT ' + self.account_token
        }
        url = self.host_url + '/1/c/' + collection_token
        r = requests.get(url=url, headers=headers)
        print(r.status_code)
        if r.status_code == 200:
            return json.loads(r.text)

    def get_collection_by_id(self, id):

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.api_token
        }

        url = "https://qiot.io/users/collections/" + str(id)
        r = requests.get(url=url, headers=headers)
        print("the status code was:", r.status_code)
        # print(r.text)
        if r.status_code == 200:
            return json.loads(r.text)
        pass

    def get_collection_thing_page_by_collection_id(self, id, page_no):

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.api_token
        }
        # / collections /: id / things / page /:page
        url = "https://qiot.io/users/collections/" +  str(id) + "/things" + "/page/" + str(page_no)
        r = requests.get(url=url, headers=headers)
        print("the status code was:", r.status_code)
        # print(r.text)
        if r.status_code == 200:
            return json.loads(r.text)
        pass

    def get_collections_and_things_by_collection_id(self, id):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.api_token
        }
        url = "https://qiot.io/users/collections/" + str(id) + "/collection+things"
        r = requests.get(url=url, headers=headers)
        print("the status code was:", r.status_code)
        # print(r.text)
        if r.status_code == 200:
            return json.loads(r.text)
        pass

    def delete_collection_by_id(self, id):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.api_token
        }

        url = "https://qiot.io/users/collections/" + str(id)
        r = requests.delete(url=url, headers=headers)
        print("the status code was:", r.status_code)
        # print(r.text)
        if r.status_code == 200:
            return json.loads(r.text)
        pass


    def delete_things_by_id(self, id):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.api_token
        }

        url = "https://qiot.io/users/things/" + str(id)
        r = requests.delete(url=url, headers=headers)
        print("the status code was:", r.status_code)
        # print(r.text)
        if r.status_code == 200:
            return json.loads(r.text)
        pass

    def delete_all_things_in_the_collection_by_collection_id(self, id):
        things_array = self.get_collections_and_things_by_collection_id(str(id))["collection"]["things"]
        for x in range(0, len(things_array)):
            print("Deleting thing with id", things_array[x]["id"])
            self.delete_things_by_id(things_array[x]["id"])


    def create_a_collection(self, collection_name):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.api_token
        }

        body = {"name": collection_name }

        url = "https://qiot.io/users/collections"
        r = requests.post(url=url, headers=headers, json=body)
        print("the status code was:", r.status_code)
        # print(r.text)
        if r.status_code == 200 :
            response = json.loads(r.text)
            print(response)
            return response["collection"]["collection_token"]
        pass

    def get_config(self):
        with open(self.config_file) as config_file:
            config = json.load(config_file)
        return config

    def get_thing_token(self, keys_file):
        with open(keys_file) as registration_config_file:
            configs = json.load(registration_config_file)
        return configs["thing"]["thing_token"]