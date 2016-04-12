import threading
import time


def init(comm_thread):
    threading.Thread(target=async, args=(comm_thread,)).start()
    comm_thread.register(process)
    process.name = 'asktime'


def async(comm_thread):
    while 1:
        time.sleep(1800)
        comm_thread.send_now("TIME\r\n")


def process(comm_thread, line, line_list, message_on_channel, lock, data):
    if line_list[1] == '391':
        try:
            ts = int(line_list[4])
        except ValueError as e:
            # Thursday March 31 2016 -- 09:28:47 +00:00
            ts = time.mktime(time.strptime(' '.join(line_list[4:]), ':%A %B %d %Y -- %H:%M:%S +00:00'))
        comm_thread.send_to_channel("Time difference with server {0:.2f}".format(time.mktime(time.gmtime()) - ts))
        return True
    return False
