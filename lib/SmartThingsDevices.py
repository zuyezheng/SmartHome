import requests


class SmartThingsDevices:
    """ Helps traverse devices list. """

    @staticmethod
    def from_json(json, smart_things):
        return SmartThingsDevices(
            list(map(
                lambda i: Device(i, smart_things),
                json['items']
            )),
            smart_things
        )

    def __init__(self, devices, smart_things):
        self.devices = devices
        self.smart_things = smart_things

    def named_like(self, name):
        """ Return a new Devices object filtered to those with a partial name match. """
        name = name.lower()

        return SmartThingsDevices(
            list(filter(
                lambda d: name in d.label().lower(),
                self.devices
            )),
            self.smart_things
        )

    def with_capability(self, capability_id):
        """ Return a new Devices object filtered to those at least 1 component supporting the given capability. """
        return SmartThingsDevices(
            list(filter(
                lambda d: len(d.components_with_capability(capability_id)) > 0,
                self.devices
            )),
            self.smart_things
        )


class Device:

    def __init__(self, json, smart_things):
        self.json = json
        self.smart_things = smart_things

    def id(self):
        return self.json['deviceId']

    def label(self):
        return self.json['label']

    def components_with_capability(self, capability_id):
        return list(filter(
            lambda component: next(
                component['id'] for capability in component['capabilities'] if capability['id'] == capability_id
            ),
            self.json['components']
        ))

    def status(self):
        """ https://smartthings.developer.samsung.com/docs/api-ref/st-api.html#operation/getDeviceStatus """
        return requests.get(
            f'https://api.smartthings.com/v1/devices/{self.id()}/status',
            headers=self.smart_things.auth_header
        ).json()

    def capability_status(self, component_id, capability_id):
        """ https://smartthings.developer.samsung.com/docs/api-ref/st-api.html#operation/getDeviceStatusByCapability """
        return requests.get(
            f'https://api.smartthings.com/v1/devices/{self.id()}/components/{component_id}/capabilities/{capability_id}/status',
            headers=self.smart_things.auth_header
        ).json()

    def command(self, component_id, capability_id, command, arguments=None):
        """ https://smartthings.developer.samsung.com/docs/api-ref/st-api.html#operation/executeDeviceCommands """

        if arguments is None:
            arguments = []

        return requests.post(
            f'https://api.smartthings.com/v1/devices/{self.id()}/commands',
            headers=self.smart_things.auth_header,
            json={
                'commands': [{
                    'component': component_id,
                    'capability': capability_id,
                    'command': command,
                    'arguments': arguments
                }]
            }
        ).json()
