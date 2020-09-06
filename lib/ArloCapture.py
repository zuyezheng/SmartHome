import sys
import time
from threading import Thread, Event

from arlo import Arlo
from requests import HTTPError


class ArloThread(Thread):

    def __init__(self, event, username, password, interval, snapshot_dir, camera_names):
        Thread.__init__(self)

        self._stopped = event
        self._username = username
        self._password = password
        self._interval = interval
        self._snapshot_dir = snapshot_dir
        self._camera_names = camera_names

    def run(self):
        self._capture()
        while not self._stopped.wait(self._interval):
            self._capture()

    def _capture(self):
        print(f'Starting capture.')
        try:
            arlo = Arlo(self._username, self._password)

            base_stations = arlo.GetDevices('basestation')
            cameras = arlo.GetDevices('camera', filter_provisioned=True)

            for camera in cameras:
                name = camera['deviceName']
                if self._camera_names is not None and name not in self._camera_names:
                    continue

                print(f'- Taking snapshot from {name}')
                url = arlo.TriggerFullFrameSnapshot(base_stations[0], camera)

                if url is not None:
                    file_name = name + '_' + str(time.time())
                    file_name = file_name.replace(' ', '_')

                    arlo.DownloadSnapshot(url, f'{self._snapshot_dir }/{file_name}.jpg')
                else:
                    print(f'-- Snapshot failed from {name}.')
        except HTTPError as e:
            print(f'Error during capture: {e}.')

class ArloCapture(Thread):

    def __init__(self, username, password, interval, snapshot_dir='', camera_names=None):
        Thread.__init__(self)

        self._stopFlag = Event()
        self._thread = ArloThread(self._stopFlag, username, password, interval, snapshot_dir, camera_names)

    def start(self):
        self._thread.start()

    def stop(self):
        self._stopFlag.set()
