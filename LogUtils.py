from etc import environment
import logging
import os
import time


def getCurrentTime():
    currTime = time.strftime("%Y-%m-%d-%H", time.gmtime())
    return currTime


def updateLogFile():
    logging.basicConfig(filename=environment.LOG_DIR + getCurrentTime() + ".log",
                        level=logging.INFO,
                        format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s')
    logging.getLogger().addHandler(logging.StreamHandler())


if not os.path.exists(environment.LOG_DIR):
    print("Creating log directory at: " + environment.LOG_DIR)
    os.makedirs(environment.LOG_DIR, exist_ok=True)

updateLogFile()
