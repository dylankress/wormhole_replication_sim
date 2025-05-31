# wormhole_replication_sim.py

from config import SIMULATION_TICKS, REPLICATION_FACTOR, MAX_REPLICATION_FACTOR, SIMULATION_CYCLES
from host_generator import generate_hosts
from simulation_clock import SimulationClock
from uploader import Uploader
from downloader import Downloader

# Global mutable replication factor
current_replication_factor = REPLICATION_FACTOR

def run_simulation(replication_factor):
    print(f"Starting simulation with REPLICATION_FACTOR = {replication_factor}")

    clock = SimulationClock()
    hosts = generate_hosts(replication_factor=replication_factor, seed_offset=replication_factor)

    print("Generated Hosts:")
    for host in hosts:
        print(host)

    uploader = Uploader()
    wait_ticks = uploader.upload_file(hosts, seed_offset=replication_factor)

    upload_attempted = False
    downloader = None

    while clock.current_tick < SIMULATION_TICKS:
        for host in hosts:
            host.cycle_uptime()

        if not upload_attempted and clock.current_tick >= wait_ticks:
            uploader.attempt_upload(hosts)
            file_ready_tick = clock.current_tick
            downloader = Downloader(file_ready_tick, seed_offset=replication_factor)
            upload_attempted = True

        if downloader and clock.current_tick >= downloader.download_try_tick:
            downloader.download_file(hosts)
            downloader = None  # Prevent multiple download attempts

        clock.tick()

    print(f"Completed {SIMULATION_TICKS} ticks with REPLICATION_FACTOR = {replication_factor}\n")

def main():
    global current_replication_factor

    while current_replication_factor <= MAX_REPLICATION_FACTOR:
        run_simulation(current_replication_factor)
        current_replication_factor += 1

if __name__ == "__main__":
    main()

