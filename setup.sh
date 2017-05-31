#! /bin/sh
pip3 install .
cp -n config.example.yml config.yml
"${EDITOR:-nano}" config.yml
echo "Successfully installed and configured TS3Proxy. Start it using ts3proxy"
