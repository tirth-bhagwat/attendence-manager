# importing module
import logging

# Create and configure logger1
logging.basicConfig(filename="newfile.log",
					format='%(asctime)s - [%(levelname)s] : %(message)s',
					filemode='w')

# Creating an object
logger1 = logging.getLogger()
logging.basicConfig(filename="newfile3.log",
					format='%(asctime)s - [%(levelname)s] : %(message)s',
					filemode='w')
logger2 = logging.getLogger()
# Setting the threshold of logger1 to DEBUG
logger1.setLevel(logging.DEBUG)

l2=logging.Logger()

# Test messages
logger1.debug("Harmless debug Message")
logger1.info("Just an information")
logger1.warning("Its a Warning")
logger1.error("Did you try to divide by zero")
logger1.critical("Internet is down")

try:
    x=5/0
except Exception as e:
    print(e)
    logger2.error(e,exc_info=True)

