from random import randint
from hashlib import md5
import socket
import string
import time

"""
This is the proof of concept, after it worked, I refactored it in ircbot.py
"""

HOST = "euroserv.fr.quakenet.org"
PORT = 6667
NICK = "Kabot"
IDENT = "Kabot"
REALNAME = "Kabot"
CHANNEL = "#" + md5(time.strftime('%Y%m%d')).hexdigest()

s = socket.socket()
s.connect((HOST, PORT))
readbuffer = ""

while 1:
    time.sleep(0.1)
    try:
        readbuffer = readbuffer + s.recv(1024)
    except socket.error:
        s.close()
        s = socket.socket()
        s.connect((HOST, PORT))
        readbuffer = ""
    temp = string.split(readbuffer, "\n")
    readbuffer = temp.pop()

    for line in temp:
        line = string.rstrip(line)
        print line
        if line == 'NOTICE AUTH :*** Found your hostname':
            s.send("NICK %s\r\n" % NICK)
            s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))

        if 'Overridden by other sign on' in line:
            s.close()

        line = string.split(line)

        if line[1] in ('433', '451'):
            try:
                s.send("NICK %s\r\n" % NICK)
            except socket.error:
                s.close()
                s = socket.socket()
                s.connect((HOST, PORT))
                readbuffer = ""
            s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
            time.sleep(randint(5, 10))

        if line[0] == "PING":
            s.send("PONG %s\r\n" % line[1])
            s.send("TIME\r\n")

        if line[1] == '221':
            s.send("JOIN %s 12345\r\n" % CHANNEL)
            s.send("MODE %s +s\r\n" % CHANNEL)
            s.send("MODE %s +k 12345\r\n" % CHANNEL)
            # s.send("STATS\r\n")

        if line[1] == "PRIVMSG" and line[2] == CHANNEL:
            if line[3] == ':!list':
                name = line[0][1:].split('!')[0]
                s.send("AWAY :\r\n")
                s.send("PRIVMSG %s :LIST!!!\r\n" % name)
            if line[3] == ':!away':
                name = line[0][1:].split('!')[0]
                s.send("AWAY :Gone to lunch!!!\r\n")
