"""
This plugin manage the ping from the irc server and add the !ping command to the bot
"""


def init(comm_thread):
    comm_thread.register(process)
    process.name = 'ping'
    comm_thread.add_help('''!ping - reply with pong''')


def process(comm_thread, line, line_list, message_on_channel, lock, data):
    if line_list[0] == "PING":
        comm_thread.send("PONG %s\r\n" % line_list[1])
        return True
    if message_on_channel and message_on_channel.split()[0] == "!ping":
        comm_thread.send_to_channel('pong')
        return True
    return False
