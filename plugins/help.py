def init(comm_thread):
    comm_thread.register(process)
    process.name = 'help'
    comm_thread.add_help('''!help - this help''')


def process(comm_thread, line, line_list, message_on_channel, lock, data):
    if message_on_channel and message_on_channel.split()[0] == "!help":
        comm_thread.send_to_channel("HELP: List of registered commands")
        for msg in comm_thread.get_help():
            comm_thread.send_to_channel("HELP: " + msg)
        comm_thread.send_to_channel("HELP: End of list")
        return True
    return False
