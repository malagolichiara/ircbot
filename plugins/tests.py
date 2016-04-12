DISABLED = True


def init(comm_thread):
    comm_thread.register(process)
    process.name = 'tests'


def process(comm_thread, line, line_list, message_on_channel, lock, data):
    if line_list[1] == "PRIVMSG" and line[2] == comm_thread.channel:
        if line_list[3] == ':!list':
            name = line_list[0][1:].split('!')[0]
            comm_thread.send("AWAY :\r\n")
            comm_thread.send("PRIVMSG %s :LIST!!!\r\n" % name)
            return True
        if line_list[3] == ':!away':
            comm_thread.send("AWAY :Gone to lunch!!!\r\n")
            return True
    return False
