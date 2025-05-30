# downloader.py

import random
from config import DOWNLOAD_WAIT_TIME_MINUTES

class Downloader:
    def __init__(self, file_ready_tick: int, seed_offset=0):
        self.file_ready_tick = file_ready_tick

        random.seed(seed_offset)
        wait_minutes = random.randint(DOWNLOAD_WAIT_TIME_MINUTES[0], DOWNLOAD_WAIT_TIME_MINUTES[1])
        wait_ticks = wait_minutes * 60  # 60 seconds per minute

        self.download_try_tick = self.file_ready_tick + wait_ticks

    def download_file(self, hosts):
        available_hosts = 0
        unavailable_hosts = 0
        found_file = False

        for host in hosts:
            if host.is_online:
                available_hosts += 1
                if "test_file" in host.hosted_file:
                    found_file = True
            else:
                unavailable_hosts += 1

        if found_file:
            print(f"Download Succeeded: {available_hosts} hosts available, {unavailable_hosts} hosts unavailable.")
        else:
            print(f"Download Failed: {available_hosts} hosts available, {unavailable_hosts} hosts unavailable.")

