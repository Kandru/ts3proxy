#! /usr/bin/env python3
# coding: utf-8

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
        ts3Udp = Udp(
            int(config['ts3server']['relayPort']),
            config['ts3server']['remoteAddr'],
            int(config['ts3server']['remotePort'])
        )
        ts3Filetransfer = Tcp(
            int(config['ts3FileTransfer']['relayPort']),
            config['ts3FileTransfer']['remoteAddr'],
            int(config['ts3FileTransfer']['remotePort'])
        )
        ts3Serverquery = Tcp(
            int(config['ts3ServerQuery']['relayPort']),
            config['ts3ServerQuery']['remoteAddr'],
            int(config['ts3ServerQuery']['remotePort'])
        )
        t1 = threading.Thread(target=ts3Udp.relay)
        t1.start()
        t2 = threading.Thread(target=ts3Filetransfer.relay)
        t2.start()
        t3 = threading.Thread(target=ts3Serverquery.relay)
        t3.start()
    except KeyboardInterrupt:
        exit(0)

if __name__ == '__main__':
    main()
