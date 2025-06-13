import time
import threading
import file_utils as file_utils
from gpiozero import OutputDevice, DigitalInputDevice
from datetime import datetime

# Constants
DURATION = 3  # seconds
PULSES_PER_LITER = 537  # Replace per meter if needed

"""
PUMP1   = 13
SOL1    = 26
FLOW1   = 24
PULSE   = 536 

PUMP2   = 17
SOL2    =  19
FLOW2   = 25
PULSE   = 537
"""
FLOW_PINS = [24,25]  # Replace with actual GPIOs
RELAY_PINS = [13,26,17,19]   # Replace with actual GPIOs

class FlowMeter:
    def __init__(self, pin, pulses_per_liter=100, name="PUMP"):
        self.pulse_count = 0
        self.total_volume = 0.0
        self.pulses_per_liter = pulses_per_liter
        self.name = name
        self.sensor = DigitalInputDevice(pin, pull_up=True)
        self.sensor.when_activated = self._on_pulse

    def _on_pulse(self):
        self.pulse_count += 1

    def monitor(self, duration):
        self.pulse_count = 0
        start_time = time.time()
        time.sleep(duration)
        end_time = time.time()

        elapsed = end_time - start_time
        volume = self.pulse_count / self.pulses_per_liter
        flow_rate = (volume / elapsed) * 60  # L/min
        self.total_volume += volume

        return {
            "pump": self.name,
            "start": datetime.fromtimestamp(start_time),
            "end": datetime.fromtimestamp(end_time),
            "elapsed_ms": round(elapsed * 1000, 2),
            "flow_rate": round(flow_rate, 3),
            "volume": round(volume, 3),
            "total_volume": round(self.total_volume, 3),
            "pulses": self.pulse_count
        }

def monitor_flow_thread(flow_meter, duration, results, idx):
    results[idx] = flow_meter.monitor(duration)

# Create flow meters and relays
flow_meters = [FlowMeter(pin, PULSES_PER_LITER, name=f"PUMP_{i+1}") for i, pin in enumerate(FLOW_PINS)]
relays = [OutputDevice(pin, active_high=False) for pin in RELAY_PINS]

try:
    if file_utils.run_file_checks():
        while True:
            print("Starting pump cycle...\n")
            # Turn on all pumps
            for relay in relays:
                relay.on()

            threads = []
            results = [None] * len(flow_meters)

            # Start monitoring in parallel
            for i, meter in enumerate(flow_meters):
                t = threading.Thread(target=monitor_flow_thread, args=(meter, DURATION, results, i))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

            # Turn off all pumps
            for relay in relays:
                relay.off()

            # Print results
            for result in results:
                result["start"] = result["start"].isoformat()
                result["end"] = result["end"].isoformat()
                file_utils.append_to_file(result)

                print(result)

            time.sleep(5)  # Wait before next cycle

except KeyboardInterrupt:
    print("Exiting...")
finally:
    for relay in relays:
        relay.off()
