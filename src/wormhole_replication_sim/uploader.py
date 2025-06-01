# uploader.py

import random
from config import UPLOAD_WAIT_TIME_MINUTES, NUMBER_OF_CHUNKS

class Uploader:
    def __init__(self):
        self.file = "test_file"

    def upload_file(self, hosts, seed_offset=0):
        # Deterministic random wait time
        random.seed(seed_offset)
        wait_minutes = random.randint(UPLOAD_WAIT_TIME_MINUTES[0], UPLOAD_WAIT_TIME_MINUTES[1])
        wait_ticks = wait_minutes * 60  # 60 seconds per minute

        print(f"Uploader will wait {wait_ticks} ticks before attempting upload...")

        return wait_ticks

    def attempt_upload(self, hosts, replication_factor):
        """
        Improved upload: pick only online hosts at upload time.
        """
        # 🆕 Find all currently online hosts
        online_hosts = [host for host in hosts if host.is_online]

        if not online_hosts:
            print("No hosts are online at upload time! Upload will fail completely.")
            return {
                'successes': 0,
                'failures': replication_factor * NUMBER_OF_CHUNKS,
                'success_rate': 0.0
            }

        total_upload_attempts = 0
        total_successful_uploads = 0

        for chunk_id in range(NUMBER_OF_CHUNKS):
            for _ in range(replication_factor):
                # 🆕 Choose from *only* online hosts
                chosen_host = random.choice(online_hosts)
                chosen_host.hosted_chunks.add(chunk_id)
                total_upload_attempts += 1
                total_successful_uploads += 1  # Since we're only picking online hosts, assume success.

        success_rate = (total_successful_uploads / total_upload_attempts) * 100 if total_upload_attempts > 0 else 0

        print(f"Upload Attempt: {total_successful_uploads} successes, {total_upload_attempts - total_successful_uploads} failures ({success_rate:.2f}% success rate)")

        return {
            'successes': total_successful_uploads,
            'failures': total_upload_attempts - total_successful_uploads,  # should always be 0 now
            'success_rate': success_rate
        }

