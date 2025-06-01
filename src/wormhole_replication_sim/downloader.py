# downloader.py

import random
from config import DOWNLOAD_WAIT_TIME_MINUTES, NUMBER_OF_CHUNKS

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

        # Count available and unavailable hosts
        for host in hosts:
            if host.is_online:
                available_hosts += 1
            else:
                unavailable_hosts += 1

        # Try to find each chunk
        all_chunks_available = True
        for chunk_id in range(NUMBER_OF_CHUNKS):
            found = any(
                host.is_online and (chunk_id in host.hosted_chunks)
                for host in hosts
            )
            if not found:
                all_chunks_available = False
                break  # no need to check further — file is unrecoverable

        if all_chunks_available:
            print(f"Download Succeeded: {available_hosts} hosts available, {unavailable_hosts} hosts unavailable.")
        else:
            print(f"Download Failed: {available_hosts} hosts available, {unavailable_hosts} hosts unavailable.")

        return {
            'success': all_chunks_available,
            'available_hosts': available_hosts,
            'unavailable_hosts': unavailable_hosts
        }

