import time
import threading
import file_utils as file_utils
from gpiozero import OutputDevice, DigitalInputDevice
from datetime import datetime

# Constants
DURATION = 15  # Duration of the monitoring cycle in seconds
PULSES_PER_LITER = 537  # Number of pulses that correspond to 1 liter of flow (specific to flow sensor used)

"""
GPIO Pin Mappings (commented reference for different setups)

PUMP1   = 13
SOL1    = 26
FLOW1   = 24
PULSE   = 536 

PUMP2   = 17
SOL2    = 19
FLOW2   = 25
PULSE   = 537
"""

# GPIO pins for flow sensors
FLOW_PINS = [24, 25]  # Replace with actual GPIOs used for each flow sensor

# GPIO pins for relays controlling pumps/valves
RELAY_PINS = [13, 26, 17, 19]  # Replace with actual GPIOs connected to relays

class FlowMeter:
    def __init__(self, pin, pulses_per_liter=100, name="PUMP"):
        """
        Initialize the flow meter object.

        Args:
            pin (int): GPIO pin connected to the flow sensor.
            pulses_per_liter (int): Calibration value for sensor (pulses per liter).
            name (str): Identifier for the pump/sensor.
        """
        self.pulse_count = 0
        self.total_volume = 0.0
        self.pulses_per_liter = pulses_per_liter
        self.name = name
        self.sensor = DigitalInputDevice(pin, pull_up=True)
        self.sensor.when_activated = self._on_pulse  # Register callback for pulse event

    def _on_pulse(self):
        """Internal callback triggered on each pulse detected from the sensor."""
        self.pulse_count += 1

    def monitor(self, duration):
        """
        Monitor flow for a specified duration.

        Args:
            duration (int): Duration in seconds to monitor the flow.

        Returns:
            dict: Dictionary containing flow data and statistics.
        """
        self.pulse_count = 0  # Reset pulse counter at start
        start_time = time.time()
        time.sleep(duration)  # Sleep while pulses accumulate
        end_time = time.time()

        elapsed = end_time - start_time
        volume = self.pulse_count / self.pulses_per_liter  # Calculate volume in liters
        flow_rate = (volume / elapsed) * 60  # Convert to liters per minute
        self.total_volume += volume  # Update cumulative volume

        return {
            "pump": self.name,
            "start": datetime.fromtimestamp(start_time),
            "end": datetime.fromtimestamp(end_time),
            "elapsed_ms": round(elapsed * 1000, 2),  # Duration in milliseconds
            "flow_rate": round(flow_rate, 3),
            "volume": round(volume, 3),
            "total_volume": round(self.total_volume, 3),
            "pulses": self.pulse_count
        }

def monitor_flow_thread(flow_meter, duration, results, idx):
    """
    Thread function to monitor a specific flow meter.

    Args:
        flow_meter (FlowMeter): The flow meter instance to monitor.
        duration (int): Duration to monitor.
        results (list): Shared list to store results.
        idx (int): Index to store the result in the shared list.
    """
    results[idx] = flow_meter.monitor(duration)

# Create flow meter instances for each defined flow pin
flow_meters = [FlowMeter(pin, PULSES_PER_LITER, name=f"PUMP_{i+1}") for i, pin in enumerate(FLOW_PINS)]

# Initialize relay control objects for each relay pin (active_low relays)
relays = [OutputDevice(pin, active_high=False) for pin in RELAY_PINS]

try:
    # Check if preconditions/files are OK before starting loop
    if file_utils.run_file_checks():
        while True:
            print("Starting pump cycle...\n")

            # Turn on all relays (start pumps/valves)
            for relay in relays:
                relay.on()

            threads = []
            results = [None] * len(flow_meters)  # Placeholder list for threaded results

            # Start one thread per flow meter to monitor simultaneously
            for i, meter in enumerate(flow_meters):
                t = threading.Thread(target=monitor_flow_thread, args=(meter, DURATION, results, i))
                threads.append(t)
                t.start()

            # Wait for all monitoring threads to finish
            for t in threads:
                t.join()

            # Turn off all relays (stop pumps/valves)
            for relay in relays:
                relay.off()

            # Process and log the flow results
            for result in results:
                # Convert datetime objects to ISO format for serialization
                result["start"] = result["start"].isoformat()
                result["end"] = result["end"].isoformat()
                file_utils.append_to_file(result)  # Save result to file

                print(result)  # Print result to console

            time.sleep(5)  # Pause before starting next cycle

except KeyboardInterrupt:
    # Graceful exit on CTRL+C
    print("Exiting...")
finally:
    # Ensure all relays are turned off upon exit
    for relay in relays:
        relay.off()
