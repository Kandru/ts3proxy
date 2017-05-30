#! /usr/bin/env python3
# coding: utf-8

import logging
import sys
import threading
import yaml

from .udp import Udp
from .tcp import Tcp
from .weblist import Weblist
from .statistics import Statistics


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
        statistics = Statistics(
            config['system']['maxUsers']
        )
        if config['ts3server']['enabled']:
            ts3_server_args = [
                logging,
                statistics,
                config['ts3server']['relayAddress'],
                int(config['ts3server']['relayPort']),
                config['ts3server']['remoteAddress'],
                int(config['ts3server']['remotePort']),
                config['ts3server']['blacklist'],
                config['ts3server']['whitelist']
            ]
            ts3_server = Udp(*ts3_server_args)
            t1 = threading.Thread(target=ts3_server.relay)
            t1.start()
            logging.info('Voice: {2}:{3} <-> {4}:{5}'.format(*ts3_server_args))
        if config['ts3FileTransfer']['enabled']:
            file_transfer_args = [
                logging,
                config['ts3FileTransfer']['relayAddress'],
                int(config['ts3FileTransfer']['relayPort']),
                config['ts3FileTransfer']['remoteAddress'],
                int(config['ts3FileTransfer']['remotePort']),
                config['ts3FileTransfer']['blacklist'],
                config['ts3FileTransfer']['whitelist']
            ]
            file_transfer = Tcp(*file_transfer_args)
            t2 = threading.Thread(target=file_transfer.relay)
            t2.start()
            logging.info('FileTransfer: {1}:{2} <-> {3}:{4}'.format(*file_transfer_args))
        if config['ts3ServerQuery']['enabled']:
            server_query_args = [
                logging,
                config['ts3ServerQuery']['relayAddress'],
                int(config['ts3ServerQuery']['relayPort']),
                config['ts3ServerQuery']['remoteAddress'],
                int(config['ts3ServerQuery']['remotePort']),
                config['ts3ServerQuery']['blacklist'],
                config['ts3ServerQuery']['whitelist']
            ]
            server_query = Tcp(*server_query_args)
            t3 = threading.Thread(target=server_query.relay)
            t3.start()
            logging.info('ServerQuery: {1}:{2} <-> {3}:{4}'.format(*server_query_args))
        if config['system']['announceServer']:
            weblist_server_args = [
                logging,
                statistics,
                config['system']['serverName'],
                config['ts3server']['relayPort'],
                config['system']['maxUsers']
            ]
            weblist_server = Weblist(*weblist_server_args)
            t4 = threading.Thread(target=weblist_server.loop)
            t4.start()
            logging.info('Weblist: Name:{2}, Port:{3}, MaxUsers: {4}'.format(*weblist_server_args))
    except KeyboardInterrupt:
        exit(0)

if __name__ == '__main__':
    main()
