"""

This plugin answer to the !stats command and send the STATS command to the IRC server.

"""

waiting_response = False


def init(comm_thread):
    comm_thread.register(process)
    process.name = 'stats'
    comm_thread.add_help('''!stats - reply with output of STATS irc command''')


def process(comm_thread, line, line_list, message_on_channel, lock, data):
    if waiting_response and line_list[1] == "NOTICE" and line_list[2] == comm_thread.config['nick']:
        comm_thread.send_to_channel("stats: %s" % (' '.join(line_list[3:])))
        return True
    if waiting_response and line_list[1] == "219" and line_list[2] == comm_thread.config['nick']:
        global waiting_response
        waiting_response = False
        return True
    if message_on_channel and message_on_channel.split()[0] == "!stats":
        comm_thread.sendcrlf('STATS')
        global waiting_response
        waiting_response = True
        return True
    return False
