# Raspberry Pi Flow Meter Monitoring System

This project is a Python-based flow monitoring and control system using a Raspberry Pi. It controls multiple pumps and SOLENOID enoid valves via relays and measures liquid flow using flow sensors. It logs volume, flow rate, and pulse data for each cycle.

## Features

- Controls multiple pumps/valves using GPIO relays
- Monitors multiple flow sensors in parallel using threading
- Calculates flow rate (L/min) and volume (L) per cycle
- Logs time-stamped flow data to file
- Modular and scalable design
- Graceful shutdown on interrupt (e.g. CTRL+C)

---

## Hardware Requirements

- Raspberry Pi (any model with GPIO support)
- Flow sensors
- Relay module (active-low)
- Pumps or SOLENOID enoid valves
- External power supply for pumps/valves
- Pull-up resistors (if not using internal pull-up)

## GPIO Pin Mapping

Edit `FLOW_PINS` and `RELAY_PINS` in the script according to your wiring.

Example configuration:
```

PUMP1  = GPIO 13
SOLENOID 1   = GPIO 26
FLOW1  = GPIO 24
````
````
PUMP2  = GPIO 17
SOLENOID 2   = GPIO 19
FLOW2  = GPIO 25

````

```python
FLOW_PINS = [24, 25]
RELAY_PINS = [13, 26, 17, 19]
````
---

## Final Pin Assignment Table

| Component | GPIO | Direction | Description                   |
| --------- | ---- | --------- | ----------------------------- |
| **PUMP 1** | 13   | Output    | Relay for Pump 1     |
| **SOLENOID 1**  | 26   | Output    | Relay for SOLENOID enoid 1 |
| **PUMP 2** | 17   | Output    | Relay for Pump 2     |
| **SOLENOID 2**  | 19   | Output    | Relay for SOLENOID enoid 2 |
| **PUMP 3** | 5    | Output    | Relay for Pump 3        |
| **SOLENOID 3**  | 6    | Output    | Relay for SOLENOID enoid 3    |
| **PUMP 4** | 16   | Output    | Relay for Pump 4        |
| **SOLENOID 4**  | 20   | Output    | Relay for SOLENOID enoid 4    |
| **FLOW METER 1** | 24   | Input     | Flow sensor 1        |
| **FLOW METER 2** | 25   | Input     | Flow sensor 2        |
| **FLOW METER 3** | 12   | Input     | Flow sensor 3           |
| **FLOW METER 4** | 21   | Input     | Flow sensor 4           |

---

### Notes

* All selected pins are standard GPIOs with **no critical system functions**.
* Avoid pins used for I²C (GPIO 2, 3), UART (GPIO 14, 15), and SPI (GPIO 10, 9, 11).
* All relays are assumed to be **active-low** and controlled using `gpiozero.OutputDevice`.
* All flow meters use **digital pulse signals** and are read using `gpiozero.DigitalInputDevice`.

## Installation

1. **Install Dependencies**

```bash
pip install gpiozero
```

2. **Project Structure**

```
project/
│
├── flow_monitor.py     # Main script
├── file_utils.py       # File handling and logging utilities
└── log.csv             # Output file (optional, auto-created)
```

> Make sure `file_utils.py` implements the `run_file_checks()` and `append_to_file()` functions used in the main script.

3. **Run the Script**

```bash
python3 app.py
```

Press `CTRL+C` to safely stop the process.

---

## Data Output

Each pump cycle logs a dictionary with the following keys:

* `pump`: Name of the pump (e.g., "PUMP\_1")
* `start`: Start time (ISO 8601 format)
* `end`: End time (ISO 8601 format)
* `elapsed_ms`: Monitoring duration in milliseconds
* `flow_rate`: Flow rate in liters per minute
* `volume`: Volume measured in this cycle (liters)
* `total_volume`: Cumulative volume for the pump
* `pulses`: Number of pulses detected

---

Here’s an improved and clearer version of your **Data Download** section for the `README.md`, with better structure, formatting, and instructions:

---

##  Data Download

To download the generated log files (e.g., `2025-01-01.csv`) from your Raspberry Pi over the local network, you can use Python’s built-in HTTP server.

### Steps

1. **Navigate to the `/data` directory** in your project:

```bash
cd ~/Documents/projects/sypp/data
```

2. **Check your Raspberry Pi’s IP address** (look for `inet` under `wlan0`):

```bash
ip addr show wlan0
```

Example output:

```
inet 192.168.1.42/24 brd 192.168.1.255 scope global dynamic wlan0
```

3. **Start a local web server** on port 8000:

```bash
python3 -m http.server
```

You should see:

```
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

4. **Download your data** from another device on the same network by visiting:

```
http://<RPI_IP_ADDRESS>:8000/
```

Example:

```
http://192.168.1.42:8000/
```
---

## Safety Notes

* Ensure the pumps and relays are powered correctly and safely.
* Use opto-iSOLENOID ated relay boards to protect your Raspberry Pi GPIOs.
* If controlling high-power devices, follow proper electrical safety practices.

---

## License

MIT License. Feel free to use and modify this project.

---

## Author

Developed by [Crysthoffer Ratier](https://github.com/crysthofferattier) @ Marco Beverage Systems Ltd.
Based on Raspberry Pi GPIO and multithreaded flow monitoring concepts.