# TS3Proxy

TS3Proxy aims to be a complete solution for proxy ts3. It allows you to hide the original location of your teamspeak server and may be a good choice to defeat DDoS-Attacks. Just use multiple instances for different kind of people (like admins, moderators, members and guests) on different virtual machines (in different data centers of course).

  - Proxy TS3 UDP Port
  - Proxy TS3 Filetransfer Port
  - Proxy TS3 Serverquery Port

## HowTo install

Just unzip the latest release (or master branch) zip file open a terminal in this folder:

pip3 install -e .

And just run it afterwards with an NON-ROOT user via command line:

ts3proxy

## HowTo run (Alternative)

If you have installed all dependencies you can just run it with:

python3 -m ts3proxy.ts3proxy