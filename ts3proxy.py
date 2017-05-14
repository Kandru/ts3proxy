#! /usr/bin/env python3
# coding: utf-8

import threading

from proxy.udp import udp
from proxy.tcp import tcp

if __name__ == '__main__':
    try:
        ts3Udp = udp(9987, '89.163.157.103', 9987)
        ts3Filetransfer = tcp(30033, '89.163.157.103', 30033)
        ts3Serverquery = tcp(10011, '89.163.157.103', 10011)
        t1 = threading.Thread(target = ts3Udp.relay)
        t1.start()
        t2 = threading.Thread(target = ts3Filetransfer.relay)
        t2.start()
        t3 = threading.Thread(target = ts3Serverquery.relay)
        t3.start()
    except KeyboardInterrupt:
        exit(0)