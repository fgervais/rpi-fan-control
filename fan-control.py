import time
import pigpio
import logging
import signal
import yaml
import argparse

from gpiozero import CPUTemperature
from fan import Fan, Controller
from pprint import pformat


PWM_PIN = 12
CONFIG_FILE = "config.yml"


def teardown():
    logger.info("Teardown")
    pi.set_mode(12, pigpio.INPUT)
    pi.set_pull_up_down(12, pigpio.PUD_DOWN)
    pi.stop()

# Used by docker-compose down
def sigterm_handler(signal, frame):
    logger.info("Reacting to SIGTERM")
    teardown()
    exit(0)

parser = argparse.ArgumentParser()
parser.add_argument("--debug", "-d", action='store_true')
args = parser.parse_args()

logging.basicConfig(
    format='[%(asctime)s] %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
if args.debug:
    logger.setLevel(logging.DEBUG)

signal.signal(signal.SIGTERM, sigterm_handler)

pi = pigpio.pi()
if not pi.connected:
    logger.error("Could not connect to pigpio")
    exit(1)

cpu = CPUTemperature()
fan = Fan(pi, PWM_PIN)

with open(CONFIG_FILE, 'r') as stream:
    config = yaml.safe_load(stream)

controller = Controller(config)

logger.debug(pformat(config))

while True:
    temperature = cpu.temperature
    required_speed = controller.required_speed(temperature)
    logger.debug("{}: {}".format(temperature, required_speed))
    fan.speed = required_speed
    time.sleep(5)
