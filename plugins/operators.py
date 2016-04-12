import threading
import time

OPLIST = (
    'chiara',
    'roberto',
)


def init(comm_thread):
    threading.Thread(target=async, args=(comm_thread,)).start()
    comm_thread.register(process)
    process.name = 'operators'


def process(comm_thread, line, line_list, message_on_channel, lock, data):
    if line_list[1] == '353':
        for name in (x for x in ' '.join(line_list[5:])[1:].split() if x in OPLIST):
            comm_thread.send('MODE %s +o %s\r\n' % (data['channel'], name))
        return True
    if line_list[1] == 'JOIN' and line_list[2] == ':' + data['channel']:
        name = line_list[0].split('!')[0][1:]
        if name in OPLIST:
            comm_thread.send('MODE %s +o %s\r\n' % (data['channel'], name))
        return True
    return False


def async(comm_thread):
    while 1:
        time.sleep(60)
        comm_thread.send_now("NAMES %s\r\n" % comm_thread.data['channel'])
