import logging
logging.basicConfig(filename='fightLog.log', level=logging.DEBUG)


class Logger:
    @staticmethod
    def log(text):
        logging.info(text)

