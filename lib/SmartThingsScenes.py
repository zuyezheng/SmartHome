import requests


class SmartThingsScenes:

    @staticmethod
    def from_json(json, smart_things):
        return SmartThingsScenes(
            list(map(
                lambda i: Scene(i, smart_things),
                json['items']
            )),
            smart_things
        )

    def __init__(self, scenes, smart_things):
        self.scenes = scenes
        self.smart_things = smart_things

    def with_name(self, name):
        """ Return the first scene with a partial match. """
        for s in self.scenes:
            if name in s.name().lower():
                return s

        return None


class Scene:

    def __init__(self, json, smart_things):
        self.json = json
        self.smart_things = smart_things

    def id(self):
        return self.json['sceneId']

    def name(self):
        return self.json['sceneName']

    def execute(self):
        return requests.post(
            f'https://api.smartthings.com/v1/scenes/{self.id()}/execute',
            headers=self.smart_things.auth_header
        ).json()
