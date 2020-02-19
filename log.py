class Logger:
    def __init__(self, sender='', level=1):
        self.sender = sender
        self.level = level

    def error(self, message):
        if self.level <= 3:
            print('[{}/ERROR] {}'.format(self.sender, message))

    def warning(self, message):
        if self.level <= 2:
            print('[{}/WARN] {}'.format(self.sender, message))

    def info(self, message):
        if self.level <= 1:
            print('[{}/INFO] {}'.format(self.sender, message))

    def debug(self, message):
        if self.level <= 0:
            print('[{}/DEBUG] {}'.format(self.sender, message))

    def server_output(self, message):
        print('[mc-server] {}'.format(message))
