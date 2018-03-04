import logging
import os
import time

def getCurrentTime():
    currTime = time.strftime("%Y-%m-%d-%H", time.gmtime())
    return currTime

def updateLogFile():
    logging.basicConfig(filename="logs/" + getCurrentTime() + ".log", level=logging.INFO, format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s')


if not os.path.exists("logs"):
    os.mkdir("logs")

updateLogFile()
