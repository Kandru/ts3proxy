# TS3Proxy

TS3Proxy aims to be a complete solution for a TeamSpeak 3 proxy. It allows you
to hide the original location of your TeamSpeak 3 server and may be a good
choice to defeat DDoS attacks. Just use multiple instances for different kind
of people (like admins, moderators, members and guests) on different virtual
machines (in different data centers of course). And it's ideal for users that
want to hide their original client IP address.

Features:

  - Proxy TS3 UDP Port
  - Proxy TS3 Filetransfer Port
  - Proxy TS3 Serverquery Port
  - Announce Proxy to Teamspeak 3 Weblist (with working client counter)

## Configuration

TS3Proxy is configured by `config.yml`. This file contains a section for every
component of TS3Proxy.

If you are new to TS3Proxy and have a default TeamSpeak configuration,
you probably want to adjust the `remoteAddress`.

- Each component can be activated or deactivated by setting `enabled` to either
`True` or `False`.
- The `relayAddress` and `relayPort` describe the address where the proxy
listens for user data. If `relayAddress` is `0.0.0.0`, the proxy listens on
all interfaces.
- The `remoteAddress` and `remotePort` describe the TeamSpeak 3 server
address. The `remoteAddress` can be either a hostname or an IP address.

Note that the file transport has to have the same port on both sides
(`relayPort` and `remotePort`). Otherwise the file transfer will not work.


### Blacklist / Whitelist

The blacklist or whitelist can be used to ban proxy users by IP address or to only allow
specific users to use the proxy. If you use the whitelist, the blacklist will
be ignored. All entries in the whitelist will be able to use the proxy, every
other IP will be blocked.

The list files (`blacklist.txt` and `whitelist.txt`) contain one IP address
per line. The files should be created in the folder that contains `config.yml`.


## Install

The requirements of TS3Proxy are:

- Python 3
- PyYAML

Just unzip the latest release (or master branch) zip file and open a terminal
in the unzipped folder and do the following steps.

### Recommended installation

The recommended way to install TS3Proxy is using the `setup.py`. This script
automatically calls pip (the Python package manager). Pip installs the
`ts3proxy` package to the Python site-packages and creates a script called
`ts3proxy` in your executable path.

```bash
sudo ./setup.sh
```

And just run it afterwards with an NON-ROOT user via command line:

```bash
ts3proxy
```

### Alternative installation: only install dependencies

Install all dependencies:

```bash
apt-get install python3-yaml
```

If you don't want to install TS3Proxy itself, you have to start the proxy with
a more complex command:

```bash
python3 -m ts3proxy
```


### Editable installation: only for developers

If you are a developer and might want to use the `ts3proxy` script, you can
install this package in editable mode by using the `-e` option:

```bash
pip3 install -e .
```
