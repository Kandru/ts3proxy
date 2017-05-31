#! /bin/sh
pip3 install .
mv config.example.yml config.yml
"${EDITOR:-nano}" config.yml
ts3proxy
