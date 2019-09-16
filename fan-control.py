import time
import pigpio
import logging
import signal

from gpiozero import CPUTemperature
from fan import Fan


PWM_PIN = 12


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


logging.basicConfig(
    format='[%(asctime)s] %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

signal.signal(signal.SIGTERM, sigterm_handler)

pi = pigpio.pi()
if not pi.connected:
    logger.error("Could not connect to pigpio")
    exit(1)

cpu = CPUTemperature()
fan = Fan(pi, PWM_PIN)

print(cpu.temperature)

while True:
    time.sleep(1)
    fan.speed = 0.1
    print(fan.speed)
