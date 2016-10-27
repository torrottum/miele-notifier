#!/usr/bin/env python3

from bs4 import BeautifulSoup
from tabulate import tabulate
from time import sleep
import requests
from pushbullet import Pushbullet
from pushbullet.errors import InvalidKeyError
import sys
import os.path
import json

def load_config():
    if not os.path.isfile('config.json'):
        print('config.json not found, exiting ...')
        sys.exit(1)
    else:
        with open('config.json') as data_file:
            return json.load(data_file)

def list_machines(machines):
    table = []
    for m_id, machine in machines.items():
        in_use = 'Yes' if machine['in_use'] else 'No'
        table.append([m_id, machine['type'], in_use])
    print(tabulate(table, ['ID', 'Type', 'In use']))

def parse_machines(config):
    machines = {}
    r = requests.get('http://' + config['ip'] + '/LaundryState?lg=1', auth=(config['username'], config['password']))

    if r.status_code == 401:
        exit_with_msg('Wrong username or password in config.json')

    soup = BeautifulSoup(r.text, 'html.parser')
    for img in soup.find_all('img', {'src': ['pic/symbolpw.gif', 'pic/symbolpt.gif']}):
        m_id = img.parent.parent.find('b').text.replace('Machine ', '')

        machines[m_id] = {
            'in_use': True if img.parent['bgcolor'] == 'Red' else False,
            'type': 'Washer' if img['src'] == 'pic/symbolpw.gif' else 'Dryer'
        }

    return machines

def watch(config, machines):
    machines = parse_machines(config)
    new_ids = []
    print('Checking machines ...')
    for index, m_id in enumerate(config['ids']):
        machine = machines[m_id]
        if (machine['in_use']):
            new_ids.append(m_id)
            print('{} {} is in use'.format(machine['type'], m_id))
        else:
            print('{} {} not in use, sending notification'.format(machine['type'], m_id))
            notify(
                config['pushbullet_token'],
                'Laundry: {} {} is done'.format(machine['type'], m_id),
                '{} {} is now done!'.format(machine['type'], m_id)
            )

    if not len(new_ids):
        exit_with_msg('All done')

    print('Waiting 60s before next check ...')
    sleep(60)
    config['ids'] = new_ids
    watch(config, machines)

def notify(key, title, body):
    try:
        pb = Pushbullet(key)
        pb.push_note(title, body)
    except InvalidKeyError as e:
        print('Failed to send notification, invalid Pushbullet access token')

def exit_with_msg(msg, code = 0):
    print(msg)
    sys.exit(code)

def main():
    config = load_config()
    machines = parse_machines(config)

    if len(sys.argv) == 1:
        exit_with_msg('Usage: ./miele-notifier.py <machine_id>...')
    elif sys.argv[1] == 'list':
        list_machines(machines)
        sys.exit()
    else:
        config['ids'] = sys.argv[1:]
        for m_id in config['ids']:
            if m_id not in machines:
                exit_with_msg('No machine with id {}'.format(m_id), 1)

        watch(config, machines)

if __name__ == '__main__':
    main()

