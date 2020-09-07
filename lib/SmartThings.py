import requests

from lib.SmartThingsScenes import SmartThingsScenes
from lib.SmartThingsDevices import SmartThingsDevices


class SmartThings:

    @staticmethod
    def fromFile(file_name):
        with open(file_name, 'r') as tokenFile:
            token = tokenFile.read()

        return SmartThings(token)

    def __init__(self, token):
        self.auth_header = {
            'Authorization': 'Bearer ' + token
        }

    def devices(self):
        """
        Return devices as a Devices object. Does not support pagination.

        https://smartthings.developer.samsung.com/docs/api-ref/st-api.html#operation/getDevices
        """
        return SmartThingsDevices.from_json(
            requests.get(
                'https://api.smartthings.com/v1/devices',
                headers=self.auth_header
            ).json(),
            self
        )

    def scenes(self):
        return SmartThingsScenes.from_json(
            requests.get(
                'https://api.smartthings.com/v1/scenes',
                headers=self.auth_header
            ).json(),
            self
        )
