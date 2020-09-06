import argparse

from lib.SmartThings import SmartThings

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

args = parser.parse_args()
print(args.command)

smart_things = SmartThings.fromFile('token.txt')
devices = smart_things.devices().named_like(args.name).with_capability('switch')

for device in devices.devices:
    component_id = device.components_with_capability('switch')[0]['id']
    capability_value = device.capability_status(component_id, 'switch')['switch']['value']

    print(f"'{device.label()}' is '{capability_value}'.")

    command = None
    if args.command == 'toggle':
        if capability_value == 'on':
            command = 'off'
        else:
            command = 'on'
    else:
        command = args.command

    if command is None:
        print(f'--> No change.')
    else:
        device.command(component_id, 'switch', command)
        print(f"--> Setting '{command}'.")