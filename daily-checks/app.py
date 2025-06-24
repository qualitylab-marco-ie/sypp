#!/usr/bin/python3

import time
import signal
import sys

from gpiozero import OutputDevice

# Use BCM numbering (GPIO numbers)
# 26 19 6 20 13 17 5 16
RELAY_PINS = [26,19,6,20,13,17,5,16]
DEVICES = [OutputDevice(pin, active_high=False) for pin in RELAY_PINS]

def signal_handler(sig, frame):
    print("\nInterrupt received. Turning off all devices...")
    for device in DEVICES:
        device.off()
    sys.exit(0)


def test_on_off(device) -> None:
    device.on()
    print(f"Device ON")
    time.sleep(2)

    device.off()
    print(f"Device ON")
    time.sleep(1)


def main() -> None:
    for i, device in enumerate(DEVICES):
        print(f"Testing device on GPIO {RELAY_PINS[i]}")
        try:
            for x in range(2):
                test_on_off(device)
        except Exception as e:
            print(e)
        finally:
            device.off()


# Register signal handler
signal.signal(signal.SIGINT, signal_handler)
if __name__ == "__main__":
    main()