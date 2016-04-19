#!/bin/env python
# -*- coding: UTF-8 -*-
#
# (c) Chiara Malagoli
#
# v 0.0.1.3
#
# file: mailmetheerror.py
# auth: Chiara Malagoli <malagoli@gbinside.com>
# desc:
#
# --------------

import os
import socket
import ssl
import threading
import time

import plugins


class CommThread(threading.Thread):
    def __init__(self, config):
        threading.Thread.__init__(self)
        self.config = dict(config)  # copy
        self.data = dict()
        self.lock = threading.Lock()
        self.readbuffer = ""
        self.callback_list = []
        self.fallback_callback_list = []
        self.send_list = []
        self.help = []

    def _connect(self):
        s = socket.socket()
        s.connect((self.config['host'], self.config['port']))
        self.readbuffer = ""
        self.sock = ssl.wrap_socket(s, cert_reqs=ssl.CERT_REQUIRED, ca_certs=self.config['ssl']) if self.config[
            'ssl'] else s
        return self.sock

    def connect(self):
        return self._connect()

    def register(self, fx):
        self.callback_list.append(fx)

    def register_fallback(self, fx):
        self.fallback_callback_list.append(fx)

    def send(self, msg):
        self.send_list.append(msg)

    def sendcrlf(self, msg):
        self.send_list.append(msg + '\r\n')

    def send_to_channel(self, msg):
        return self.send("PRIVMSG {} :{}\r\n".format(self.config['channel'], msg.rstrip()))

    def send_now(self, msg):
        with self.lock:
            self.sock.send(msg)

    def add_help(self, help_msg):
        self.help.append(help_msg)

    def get_help(self):
        return self.help

    def run(self):
        self._connect()

        while 1:
            flood_wait = self.config.get('flood_wait', None)  # it is in the main loop so plugins can change the value.
            time.sleep(0.1)
            try:
                self.readbuffer += self.sock.recv(1024)
            except socket.error:
                self.sock.close()
                self._connect()
            temp = self.readbuffer.split("\n")
            self.readbuffer = temp.pop()

            for line in temp:
                message_on_channel = None
                line = line.rstrip()
                line_list = tuple(line.split())
                if line_list[1] == "PRIVMSG" and line_list[2] == self.config['channel'] and line_list[3][0] == ':':
                    message_on_channel = line_list[3][1:]

                print '<----', line

                for fx in self.callback_list:
                    try:
                        if fx(self, line, line_list, message_on_channel, self.lock, self.data):
                            break
                    except Exception as e:
                        self.send_to_channel('EXCEPTION: {} {}'.format(getattr(fx, 'name', fx), e.message))
                else:  # fallback
                    for fx in self.fallback_callback_list:
                        try:
                            fx(self, line, line_list, message_on_channel, self.lock, self.data)
                        except Exception as e:
                            self.send_to_channel('EXCEPTION: {} {}'.format(getattr(fx, 'name', fx), e.message))

                loop_break = False
                while not loop_break and self.send_list:
                    print '---->', self.send_list[0].rstrip()
                    with self.lock:
                        try:
                            self.sock.send(self.send_list[0])
                            self.send_list.pop(0)
                        except socket.error, e:
                            self.sock.close()
                            time.sleep(flood_wait)
                            self._connect()
                            loop_break = True
                        if flood_wait:
                            time.sleep(flood_wait)


def main(**config):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    comm_thread = CommThread(config)

    plugins.init(comm_thread)

    comm_thread.start()

    comm_thread.join()
    return 0
