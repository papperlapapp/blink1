"""
This is a demonstration of the Build Light API.
"""
import time
import random
import socket
import logging
import itertools
import zmq
from .flash import BuildLightRequest, COLOURS
from .discover import discover

log = logging.getLogger(__name__)

context = zmq.Context()

def run():
    config = discover()
    upstream_url = config['upstream']

    socket = context.socket(zmq.PUB)
    socket.connect(upstream_url)
    log.info("Publisher connected to %s" % upstream_url)

    blr = BuildLightRequest(socket)

    for i in itertools.count():
        rnd = random.random()

        if rnd > 0.25:
            # Send a flash instruction
            times = random.randint(1, 9)
            duration = random.uniform(0.2, 0.8)
            colour = random.choice(COLOURS)

            blr.flash(times=times, duration=duration, colour=colour)
        else:
            fade_time = random.randint(1,4)
            freq = 1 / fade_time
            colours = random.sample(COLOURS, random.randint(2,5))
            blr.throb(freq=freq, colours=colours)

        time.sleep(20)

def main():
    logging.basicConfig()
    logging.getLogger("").setLevel(logging.INFO)
    run()

if __name__ == '__main__':
    main()
