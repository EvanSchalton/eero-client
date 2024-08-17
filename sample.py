#!/usr/bin/env python
from argparse import ArgumentParser
import json
import eero
import six
from logging import getLogger
import os
from pathlib import Path

logger = getLogger('eero')

DEBUGGING_PATH = Path(raw_debugging_path) if (raw_debugging_path := os.get("DEBUGGING_PATH", None)) else None 
if DEBUGGING_PATH:
    DEBUGGING_PATH.mkdir(parents=True, exist_ok=True)

logger.debug("DEBUGGING_PATH: %s", DEBUGGING_PATH)

class CookieStore(eero.SessionStorage):
    def __init__(self, cookie_file):
        from os import path
        self.cookie_file = path.abspath(cookie_file)

        try:
            with open(self.cookie_file, 'r') as f:
                self.__cookie = f.read()
        except IOError:
            self.__cookie = None 

    @property
    def cookie(self):
        return self.__cookie

    @cookie.setter
    def cookie(self, cookie):
        self.__cookie = cookie
        with open(self.cookie_file, 'w+') as f:
            f.write(self.__cookie)


session = CookieStore('session.cookie')
eero = eero.Eero(session)

CHOICES = [
    'ac_compat',
    # 'burst_reporters',
    'device_blacklist',
    'devices',
    'diagnostics',
    'eeros',
    'forwards',
    # 'ouicheck',
    'guestnetwork',
    # 'password',
    'profiles',
    'reservations',
    # 'settings',
    'speedtest',
    # 'transfer',
    'updates',
    # 'reboot',
    'support',
    # 'insights',
    'routing',
    'thread',
    'cli_debug'
]


def execute_command(account, command, args=None):

    if command == "cli_debug":
        for command in CHOICES:
            if command == "cli_debug":
                continue
            if DEBUGGING_PATH:
                with open(DEBUGGING_PATH / f"{command}.json", "w+") as out_command:
                    out_command.write(json.dumps(
                        execute_command(account, command)))
        return

    for network in account['networks']['data']:
        logger.info("network: %s", network)

        if command == 'reboot':
            result = eero.reboot(args.eero)
        else:
            result = eero.__getattribute__(command)(network_id = network['url'].split("/")[-1])
        logger.debug("result: %s", json.dumps(result, indent=2))
        return result


if __name__ == '__main__':
    if eero.needs_login():
        parser = ArgumentParser()
        parser.add_argument(
            "-l", help="your eero login (email address or phone number)")
        args = parser.parse_args()
        if args.l:
            phone_number = args.l
        else:
            phone_number = six.moves.input(
                'your eero login (email address or phone number): ')
        user_token = eero.login(phone_number)
        verification_code = six.moves.input(
            'verification key from email or SMS: ')
        eero.login_verify(verification_code, user_token)
        logger.info('Login successful. Rerun this command to get some output')
    else:
        account = eero.account()

        parser = ArgumentParser()
        parser.add_argument("command",
                            choices=CHOICES,
                            help="info to print")
        parser.add_argument("--eero", type=int, help="eero to reboot")
        args = parser.parse_args()

        execute_command(account, args.command, args)

