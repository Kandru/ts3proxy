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
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc, file=sys.stderr)
            sys.exit(1)
    numeric_level = getattr(logging, config['system']['logLevel'].upper(), None)
    if numeric_level is None:
        raise ValueError('Invalid log level: %s' % config['system']['logLevel'])
    logging.basicConfig(
        level=numeric_level,
        format='[%(asctime)s] %(message)s',
        handlers=[
            logging.FileHandler(config['system']['logfile']),
            logging.StreamHandler()
        ]
    )
    statistics = Statistics(
        config['system']['maxUsers']
    )
    services = []
    if config['ts3server']['enabled']:
        ts3_config = config['ts3server']
        ts3_servers = config['ts3server']['servers']
        for item in ts3_servers.split(','):
            ts3_config['relayPort'] = int(item.split(':')[0])
            ts3_config['remoteAddress'] = item.split(':')[1]
            ts3_config['remotePort'] = int(item.split(':')[2])
            ts3_server = UdpRelay.create_from_config(logging, statistics, ts3_config)
            ts3_server.start_thread()
            services.append(ts3_server)
            logging.info('Voice: {0.relay_address}:{0.relay_port} <-> {0.remote_address}:{0.remote_port}'.format(
                ts3_server
            ))
    if config['ts3FileTransfer']['enabled']:
        file_transfer = TcpRelay.create_from_config(logging, config['ts3FileTransfer'])
        file_transfer.start_thread()
        services.append(file_transfer)
        logging.info('FileTransfer: {0.relay_address}:{0.relay_port} <-> {0.remote_address}:{0.remote_port}'.format(
            file_transfer
        ))
    if config['ts3ServerQuery']['enabled']:
        server_query = TcpRelay.create_from_config(logging, config['ts3ServerQuery'])
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
