#! /usr/bin/env python3
# coding: utf-8

import threading

from proxy.udp import udp

if __name__ == '__main__':
    try:
        u = udp(9987, '89.163.157.103', 9987)
        t = threading.Thread(target = u.relay)
        t.start()
    except KeyboardInterrupt:
        exit(0)