# uploader.py

import random
from config import UPLOAD_WAIT_TIME_MINUTES

class Uploader:
    def __init__(self):
        self.file = "test_file"

    def upload_file(self, hosts, seed_offset=0):
        # Deterministic random wait time
        random.seed(seed_offset)
        wait_minutes = random.randint(UPLOAD_WAIT_TIME_MINUTES[0], UPLOAD_WAIT_TIME_MINUTES[1])
        wait_ticks = wait_minutes * 60  # 60 seconds per minute

        print(f"Uploader will wait {wait_ticks} ticks before attempting upload...")

        # Instead of real time wait, just return wait_ticks for the simulation to wait in the main loop
        return wait_ticks

    def attempt_upload(self, hosts):
        success_count = 0
        fail_count = 0

        for host in hosts:
            if host.is_online:
                host.hosted_file.add(self.file)
                success_count += 1
            else:
                fail_count += 1

        total = success_count + fail_count
        success_rate = (success_count / total) * 100 if total > 0 else 0

        print(f"Upload Attempt: {success_count} successes, {fail_count} failures ({success_rate:.2f}% success rate)")
