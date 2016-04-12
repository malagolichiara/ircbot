def init(comm_thread):
    comm_thread.register_fallback(process)


def process(comm_thread, line, line_list, message_on_channel, lock, data):
    if message_on_channel and message_on_channel[0] == "!":
        comm_thread.send_to_channel('No plugin found for "%s"' % message_on_channel)
        return True
    return False
