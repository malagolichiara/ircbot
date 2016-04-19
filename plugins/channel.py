from random import randint
import socket
import time


def init(comm_thread):
    comm_thread.register(process)


def process(comm_thread, line, line_list, message_on_channel, lock, data):
    config = comm_thread.config
    nick_ = config['nick']
    channel_ = config['channel']
    if line in ('NOTICE AUTH :*** Found your hostname', "NOTICE AUTH :*** Couldn't look up your hostname"):
        comm_thread.send("NICK %s\r\n" % nick_)
        comm_thread.send("USER {ident} {host} bla :{realname}\r\n".format(**config))
        return True

    if line_list[1] in ('221', '422'):
        channel_password = config.get('channel_password', None)
        if channel_password is not None:
            comm_thread.send("JOIN %s %s\r\n" % (channel_, channel_password))
            comm_thread.send("MODE %s +s\r\n" % channel_)
            comm_thread.send("MODE %s +k %s\r\n" % (channel_, channel_password))
        else:
            comm_thread.send("JOIN %s\r\n" % channel_)
        # s.send("STATS\r\n")
        return True

    if 'Overridden by other sign on' in line:
        comm_thread.sock.close()
    if line_list[1] in ('433', '451'):  # nickname already in use
        try:
            with lock:
                comm_thread.sock.send("NICK %s\r\n" % nick_)
        except socket.error:
            comm_thread.sock.close()
            comm_thread.connect()
        with lock:
            comm_thread.sock.send("USER {ident} {host} bla :{realname}\r\n".format(**config))
        time.sleep(randint(5, 10))

    return False
