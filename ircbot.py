from hashlib import md5
import mailmetheerror
import threading
import plugins
import socket
import time
import sys
import ssl
import os

HOST = "euroserv.fr.quakenet.org"
PORT = 6667
NICK = "Kabot"
IDENT = "kabot"
REALNAME = "Gbinside Bot"
# CHANNEL = "#" + md5(time.strftime('%Y%m%d')).hexdigest()
CHANNEL = "#kabot"
CHANNELPASSWORD = '12345'  # or None
SSL = False  # or put the filename for the certificates


class CommThread(threading.Thread):
    def __init__(self, **kargv):
        threading.Thread.__init__(self)
        self.data = dict(kargv)
        self.lock = threading.Lock()
        self.readbuffer = ""
        self.callback_list = []
        self.fallback_callback_list = []
        self.send_list = []
        self.help = []

    def _connect(self):
        s = socket.socket()
        s.connect((self.data['host'], self.data['port']))
        self.readbuffer = ""
        self.sock = ssl.wrap_socket(s, cert_reqs=ssl.CERT_REQUIRED, ca_certs=self.data['ssl']) if self.data[
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

    def send_to_channel(self, msg):
        return self.send("PRIVMSG {} :{}\r\n".format(self.data['channel'], msg.rstrip()))

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
                if line_list[1] == "PRIVMSG" and line_list[2] == self.data['channel'] and line_list[3][0] == ':':
                    message_on_channel = line_list[3][1:]

                print '<----', line

                for fx in self.callback_list:
                    try:
                        if fx(self, line, line_list, message_on_channel, self.lock, self.data):
                            break
                    except Exception as e:
                        self.send_to_channel('EXCEPTION: {} {}'.format(fx, e.message))
                else:  # fallback
                    for fx in self.fallback_callback_list:
                        try:
                            fx(self, line, line_list, message_on_channel, self.lock, self.data)
                        except Exception as e:
                            self.send_to_channel('EXCEPTION: {} {}'.format(getattr(fx, 'name', fx), e.message))

                while self.send_list:
                    print '---->', self.send_list[0].rstrip()
                    with self.lock:
                        self.sock.send(self.send_list.pop(0))


def main(argv=None):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    comm_thread = CommThread(host=HOST, port=PORT, nick=NICK, id=IDENT, realname=REALNAME, channel=CHANNEL, ssl=SSL,
                             channel_password=CHANNELPASSWORD)

    plugins.init(comm_thread)

    comm_thread.start()

    comm_thread.join()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
