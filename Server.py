import argparse
import os
from datetime import datetime

from flask import Flask, render_template

from lib.ArloCapture import ArloCapture
from lib.SmartThings import SmartThings

app = Flask(__name__, static_url_path='/static', static_folder='static')

cameras = ['Front Door', 'Garage', 'Street']
arlo_capture = None


@app.route('/')
def home():
    files = sorted(os.listdir('static/arlo'))
    files.reverse()

    most_recent = []
    snapshots_to_find = set(map(lambda n: n.replace(' ', '_'), cameras))
    for file in files:
        if len(snapshots_to_find) == 0:
            break

        for snapshot in snapshots_to_find:
            if file.startswith(snapshot):
                most_recent.append(f'static/arlo/{file}')
                snapshots_to_find.remove(snapshot)
                break

    return render_template(
        'index.html',
        files=most_recent,
        last_snapshot=datetime.fromtimestamp(float(most_recent[0][-21: -4])).strftime("%d/%m/%y %I:%M:%S %p")
    )

@app.route('/toggle/<name>')
def toggle(name):
    smart_things = SmartThings.fromFile('token.txt')
    devices = smart_things.devices().named_like(name).with_capability('switch')

    for device in devices.devices:
        component_id = device.components_with_capability('switch')[0]['id']
        capability_value = device.capability_status(component_id, 'switch')['switch']['value']

        print(f"'{device.label()}' is '{capability_value}'.")

        if capability_value == 'on':
            command = 'off'
        else:
            command = 'on'

        if command is None:
            print(f'--> No change.')
        else:
            device.command(component_id, 'switch', command)
            print(f"--> Setting '{command}'.")

    return f'Toggled {name}.'


@app.route('/start-capture')
def start():
    arlo_capture.start()
    return 'Started.'


parser = argparse.ArgumentParser(description='Flip some switches.')
parser.add_argument(
    'command',
    type=str,
    metavar='command',
    help='On, off, or toggle.'
)
parser.add_argument(
    '--name',
    help='Switch names to look for.'
)

parser = argparse.ArgumentParser()
parser.add_argument('--arlo_username')
parser.add_argument('--arlo_password')
args = parser.parse_args()

if __name__ == "__main__":
    arlo_capture = ArloCapture(
        args.arlo_username,
        args.arlo_password,
        1800,
        'static/arlo',
        cameras
    )

    app.run()
