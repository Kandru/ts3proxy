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

        if config['ts3server']['enabled']:
          UDP = []
          UDP.append( config['ts3server']['relayAddress'] )
          UDP.append( int(config['ts3server']['relayPort']) )
          UDP.append( config['ts3server']['remoteAddress'] )
          UDP.append( int(config['ts3server']['remotePort']) )
          ts3Udp = Udp(*UDP[:3])
          t1 = threading.Thread(target=ts3Udp.relay)
          t1.start()
          print("Voice: %s:%s <-> %s:%s" % UDP)

        if config['ts3FileTransfer']['enabled']:
          FT = []
          FT.append( config['ts3FileTransfer']['relayAddress'] )
          FT.append( int(config['ts3FileTransfer']['relayPort']) )
          FT.append( config['ts3FileTransfer']['remoteAddress'] )
          FT.append( int(config['ts3FileTransfer']['remotePort']) )
          ts3Filetransfer = Tcp(*FT[:3])
          t2 = threading.Thread(target=ts3Filetransfer.relay)
          t2.start()
          print("FileTransfer: %s:%s <-> %s:%s" % UDP)

        if config['ts3ServerQuery']['enabled']:
          SQ = []
          SQ.append( config['ts3ServerQuery']['relayAddress'] )
          SQ.append( int(config['ts3ServerQuery']['relayPort']) )
          SQ.append( config['ts3ServerQuery']['remoteAddress'] )
          SQ.append( int(config['ts3ServerQuery']['remotePort']) )
          ts3Serverquery = Tcp(*SQ[:3])
          t3 = threading.Thread(target=ts3Serverquery.relay)
          t3.start()
          print("ServerQuery: %s:%s <-> %s:%s" % UDP)

    except KeyboardInterrupt:
        exit(0)

if __name__ == '__main__':
    main()
