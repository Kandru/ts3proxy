#! /usr/bin/env python3
# coding: utf-8

import logging
import sys
import threading
import yaml

from .udp import Udp
from .tcp import Tcp


def main():
    try:
        with open("config.yml", 'r') as stream:
            try:
                config = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        numeric_level = getattr(logging, config['system']['logLevel'].upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % config['system']['logLevel'])
        logging.basicConfig(
            level=numeric_level,
            format='[%(asctime)s] %(message)s',
            handlers=[
                logging.FileHandler("system.log"),
                logging.StreamHandler()
            ]
        )
        if config['ts3server']['enabled']:
            ts3_server_args = [
                config['ts3server']['relayAddress'],
                int(config['ts3server']['relayPort']),
                config['ts3server']['remoteAddress'],
                int(config['ts3server']['remotePort'])
            ]
            ts3_server = Udp(*ts3_server_args[:4])
            t1 = threading.Thread(target=ts3_server.relay)
            t1.start()
            logging.info('Voice: {0}:{1} <-> {2}:{3}'.format(*ts3_server_args))
        if config['ts3FileTransfer']['enabled']:
            file_transfer_args = [
                config['ts3FileTransfer']['relayAddress'],
                int(config['ts3FileTransfer']['relayPort']),
                config['ts3FileTransfer']['remoteAddress'],
                int(config['ts3FileTransfer']['remotePort'])
            ]
            file_transfer = Tcp(*file_transfer_args[:4])
            t2 = threading.Thread(target=file_transfer.relay)
            t2.start()
            logging.info('FileTransfer: {0}:{1} <-> {2}:{3}'.format(*file_transfer_args))
        if config['ts3ServerQuery']['enabled']:
            server_query_args = [
                config['ts3ServerQuery']['relayAddress'],
                int(config['ts3ServerQuery']['relayPort']),
                config['ts3ServerQuery']['remoteAddress'],
                int(config['ts3ServerQuery']['remotePort'])
            ]
            server_query = Tcp(*server_query_args[:4])
            t3 = threading.Thread(target=server_query.relay)
            t3.start()
            logging.info('ServerQuery: {0}:{1} <-> {2}:{3}'.format(*server_query_args))
    except KeyboardInterrupt:
        exit(0)

if __name__ == '__main__':
    main()
