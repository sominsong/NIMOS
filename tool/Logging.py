import logging

class Logging:
    
    def __init__(self, lv):
        self.level = logging.INFO

        if lv == 'debug':
            self.level = logging.DEBUG
        elif lv == 'info':
            self.level = logging.INFO

        logging.basicConfig(
            format = '[%(levelname)s] %(message)s',
            level = self.level
        )

    def info(self, msg):
        logging.info(f"{msg}")

    def debug(self, msg):
        logging.debug(f"{msg}")

    def warning(self, msg):
        logging.warning(f"{msg}")

    def error(self, msg):
        logging.warning(f"{msg}")