# wormhole_replication_sim.py

from config import SIMULATION_TICKS, REPLICATION_FACTOR, MAX_REPLICATION_FACTOR, SIMULATION_CYCLES
from host_generator import generate_hosts
from simulation_clock import SimulationClock
from uploader import Uploader
from downloader import Downloader
import math
import csv
import os
from datetime import datetime

# Global mutable replication factor
current_replication_factor = REPLICATION_FACTOR

# Dynamically set CYCLE_SPACING based on SIMULATION_CYCLES
CYCLE_SPACING = 10 ** (math.ceil(math.log10(SIMULATION_CYCLES + 1)))

def run_simulation(replication_factor, writer, cycle, seed_offset):
    print(f"Starting simulation Cycle {cycle} with REPLICATION_FACTOR = {replication_factor}")

    clock = SimulationClock()
    hosts = generate_hosts(replication_factor=replication_factor, seed_offset=seed_offset)

    uploader = Uploader()
    wait_ticks = uploader.upload_file(hosts, seed_offset=seed_offset)
    print(f"Uploader scheduled to attempt at tick {wait_ticks}")

    upload_attempted = False
    downloader = None
    upload_stats = None
    download_result = None

    while clock.current_tick < SIMULATION_TICKS:
        for host in hosts:
            host.cycle_uptime()

        if not upload_attempted and clock.current_tick >= wait_ticks:
            upload_stats = uploader.attempt_upload(hosts)
            print(f"Uploader attempted at tick {clock.current_tick}")
            file_ready_tick = clock.current_tick
            downloader = Downloader(file_ready_tick, seed_offset=seed_offset)
            print(f"Downloader scheduled to attempt at tick {downloader.download_try_tick}")
            upload_attempted = True

        if downloader and clock.current_tick >= downloader.download_try_tick:
            download_result = downloader.download_file(hosts)
            print(f"Downloader attempted at tick {clock.current_tick}")
            downloader = None

        clock.tick()

    # Write result to CSV
    if upload_stats and download_result:
        print(f"Writing result for Cycle {cycle}")
        writer.writerow([
            cycle,
            replication_factor,
            upload_stats['successes'],
            upload_stats['failures'],
            f"{upload_stats['success_rate']:.2f}",
            "Success" if download_result['success'] else "Failure",
            download_result['available_hosts'],
            download_result['unavailable_hosts']
        ])
    else:
        print(f"Skipping write for Cycle {cycle} — upload_stats or download_result missing!")

    print(f"Completed Cycle {cycle} with REPLICATION_FACTOR = {replication_factor}\n")


output_dir = os.path.expanduser('~/.wormhole/simulation_results/')
os.makedirs(output_dir, exist_ok=True)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

output_file = os.path.join(output_dir, f'simulation_results_{timestamp}.csv')

def main():
    global current_replication_factor

    # Open a CSV file to save results
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'cycle', 'replication_factor',
            'upload_successes', 'upload_failures', 'upload_success_rate',
            'download_result', 'available_hosts', 'unavailable_hosts'
        ])

        while current_replication_factor <= MAX_REPLICATION_FACTOR:
            for cycle in range(1, SIMULATION_CYCLES + 1):
                seed_offset = (current_replication_factor * CYCLE_SPACING) + cycle
                run_simulation(replication_factor=current_replication_factor, writer=writer, cycle=cycle, seed_offset=seed_offset)
            current_replication_factor += 1

    print(f"\n✅ Simulation complete. Results saved to: {output_file}\n")

if __name__ == "__main__":
    main()

