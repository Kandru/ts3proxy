import logging
import sys

import yaml

from .udp import UdpRelay
from .tcp import TcpRelay
from .weblist import Weblist
from .statistics import Statistics


def main():
    with open("config.yml", 'r') as stream:
        try:
            config = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc, file=sys.stderr)
            sys.exit(1)
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
    services = []
    if config['ts3server']['enabled']:
        ts3_server = UdpRelay(
            logging,
            statistics,
            config['ts3server']['relayAddress'],
            config['ts3server']['relayPort'],
            config['ts3server']['remoteAddress'],
            config['ts3server']['remotePort'],
            config['ts3server']['blacklist'],
            config['ts3server']['whitelist']
        )
        ts3_server.start_thread()
        services.append(ts3_server)
        logging.info('Voice: {0.relay_address}:{0.relay_port} <-> {0.remote_address}:{0.remote_port}'.format(
            ts3_server
        ))
    if config['ts3FileTransfer']['enabled']:
        file_transfer = TcpRelay(
            logging,
            config['ts3FileTransfer']['relayAddress'],
            config['ts3FileTransfer']['relayPort'],
            config['ts3FileTransfer']['remoteAddress'],
            config['ts3FileTransfer']['remotePort'],
            config['ts3FileTransfer']['blacklist'],
            config['ts3FileTransfer']['whitelist']
        )
        file_transfer.start_thread()
        services.append(file_transfer)
        logging.info('FileTransfer: {0.relay_address}:{0.relay_port} <-> {0.remote_address}:{0.remote_port}'.format(
            file_transfer
        ))
    if config['ts3ServerQuery']['enabled']:
        server_query = TcpRelay(
            logging,
            config['ts3ServerQuery']['relayAddress'],
            config['ts3ServerQuery']['relayPort'],
            config['ts3ServerQuery']['remoteAddress'],
            config['ts3ServerQuery']['remotePort'],
            config['ts3ServerQuery']['blacklist'],
            config['ts3ServerQuery']['whitelist']
        )
        server_query.start_thread()
        services.append(server_query)
        logging.info('ServerQuery: {0.relay_address}:{0.relay_port} <-> {0.remote_address}:{0.remote_port}'.format(
            server_query
        ))
    if config['system']['announceServer']:
        weblist_server = Weblist(
            logging,
            statistics,
            config['system']['serverName'],
            config['ts3server']['relayPort'],
            config['system']['maxUsers']
        )
        weblist_server.start_thread()
        services.append(weblist_server)
        logging.info('Weblist: Name: {0.server_name}, Port: {0.server_port}, MaxUsers: {0.max_users}'.format(
            weblist_server
        ))

    try:
        # now all services are started
        # wait for threads to stop or for keyboard interrupt
        for service in services:
            service.thread.join()
    except KeyboardInterrupt:
        logging.info('received KeyboardInterrupt, stopping threads')
        for service in services:
            service.stop_thread()
        logging.info('closed sockets, waiting for threads to stop')
        for service in services:
            service.thread.join()
        logging.info('threads stopped')
