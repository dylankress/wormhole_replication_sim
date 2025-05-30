# host_generator.py

import random
import string
from host import Host
from config import RANDOMIZATION_SEED, REPLICATION_FACTOR, UPTIME_RANGE_MINUTES, DOWNTIME_RANGE_MINUTES

def generate_random_id(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def convert_minutes_to_ticks(minutes):
    return minutes * 60  # 60 seconds per minute → ticks

def generate_hosts(replication_factor=None, seed_offset=0):
    if replication_factor is None:
        replication_factor = REPLICATION_FACTOR

    # New: seed + offset
    random.seed(RANDOMIZATION_SEED + seed_offset)

    hosts = []

    for _ in range(replication_factor):
        host_id = generate_random_id()

        uptime_minutes = random.randint(UPTIME_RANGE_MINUTES[0], UPTIME_RANGE_MINUTES[1])
        downtime_minutes = random.randint(DOWNTIME_RANGE_MINUTES[0], DOWNTIME_RANGE_MINUTES[1])

        uptime_ticks = convert_minutes_to_ticks(uptime_minutes)
        downtime_ticks = convert_minutes_to_ticks(downtime_minutes)

        uptime_cycle_counter = random.randint(0, uptime_ticks)

        host = Host(
            host_id=host_id,
            uptime=uptime_ticks,
            downtime=downtime_ticks,
            uptime_cycle_counter=uptime_cycle_counter
        )

        hosts.append(host)

    return hosts

