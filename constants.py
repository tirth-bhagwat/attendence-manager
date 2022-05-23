import os
import logging


class Constants:
    HOME_DIR = ''
    DATA_DIR = './data'
    LOGGING_DIR = ''

    @classmethod
    def AvailableDBs(cls):
        '''Returns a list of all available databases in the DATA_DIR'''
        lst = []
        for i in list(filter(
            lambda x: True if x.endswith('.db') else False,
            os.listdir(Constants.DATA_DIR)
        )):
            lst.append(i[:-3])
        return lst

    @classmethod
    def setupLogger(cls):
        '''Sets up a logger object.'''
        logging.basicConfig(
            filename="logs.log",
            format='%(asctime)s - [%(levelname)s] : %(message)s',
            filemode='a'
        )

        Constants.LOGGER = logging.getLogger()
        Constants.LOGGER.setLevel(logging.DEBUG)
