import requests

from smartthings.Devices import Devices


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
        return Devices.from_json(
            requests.get(
                'https://api.smartthings.com/v1/devices',
                headers=self.auth_header
            ).json(),
            self
        )



