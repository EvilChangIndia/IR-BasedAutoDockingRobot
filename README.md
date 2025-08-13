# IR-BasedAutoDockingRobot

An infrared (IR) beacon–based auto docking system for mobile robots, designed to resist ambient light interference and signal strength variation. The project provides a Python-based signal-processing core; motor control must be integrated separately. Full hardware setup for the Beacon is available on Instructables: https://www.instructables.com/Automated-Docking-Using-IR/

***

## Table of Contents

1. [Features](#features)  
2. [Directory Structure](#directory-structure)  
3. [Requirements](#requirements)  
4. [Installation](#installation)  
5. [Usage](#usage)  
   - [Beacon Signal Test](#beacon-signal-test)  
   - [Automated Docking](#automated-docking)  
6. [Configuration](#configuration)  
7. [Hardware Integration](#hardware-integration)  
8. [Troubleshooting](#troubleshooting)  
9. [License](#license)  

***

## Features

- **Ambient-Light Immunity:** Uses modulated IR pulses and digital filtering to reject sunlight and indoor lighting noise.  
- **RSS Variation Compensation:** Adaptive thresholding handles fluctuations in received signal strength.  
- **Python Core:** Simple scripts for beacon testing and docking logic—easily extended or embedded.  
- **Platform Agnostic:** Runs on any Linux-capable SBC (Raspberry Pi, Jetson, etc.) with an IR receiver.  

***

## Directory Structure

```plaintext
IR-BasedAutoDockingRobot/
├── beacon_test.py       # Test script to verify IR beacon reception
├── auto_docker.py       # Main docking routine (no motor control)
├── README.md            # This file
└── LICENSE              # Project license (MIT)
```

***

## Requirements

- Python 3.6 or higher  
- `numpy`  
- `scipy`  
- An IR receiver module (e.g., TSOP38238) connected to a GPIO or ADC pin  
- Access to GPIO/ADC from Python (e.g., `RPi.GPIO`, `gpiozero`, or `Adafruit_BBIO`)  

***

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/EvilChangIndia/IR-BasedAutoDockingRobot.git
   cd IR-BasedAutoDockingRobot
   ```
2. Install Python dependencies:
   ```bash
   pip install numpy scipy
   ```
3. Wire your IR receiver to the designated input pin on your board.

***

## Usage

### Beacon Signal Test

Use `beacon_test.py` to verify that your IR receiver is detecting the modulated beacon signal.

```bash
python3 beacon_test.py --pin 
```

- `--pin`: GPIO or ADC pin number connected to the IR receiver.  
- The script displays real-time signal strength and indicates pulse detection.

### Automated Docking

Run `auto_docker.py` to start the docking routine. This script samples the IR input, computes the bearing to the beacon, and outputs steering suggestions.

```bash
python3 auto_docker.py --pin  [--interval 0.1] [--threshold 0.5]
```

- `--pin`: GPIO/ADC pin number for IR input.  
- `--interval`: Sampling interval in seconds (default: 0.05).  
- `--threshold`: Detection threshold relative to noise floor (0–1, default: 0.3).

The script logs heading angle and signal confidence; integrate its output with your robot’s motor-control code.

***

## Configuration

You can adjust parameters at the top of each script:

- `SAMPLE_RATE` (Hz)  
- `FILTER_ORDER` and `CUT_OFF_FREQ` for the digital filter  
- `BEACON_FREQ` (Hz) modulation frequency  

Modify these values to match your IR transmitter modulation and desired responsiveness.

***

## Hardware Integration

This repository provides only the sensing and signal-processing logic. To complete the docking system:

1. Mount an IR transmitter (beacon) at the docking station, modulated at the specified `BEACON_FREQ`.  
2. Interface the Python scripts’ output (bearing angle, signal strength) to motor-control routines on your platform (e.g., via ROS topics, serial commands, GPIO PWM).  
3. Tune PID or steering logic to guide wheels toward the beacon.

For a full build guide, bill of materials, and wiring diagrams, see the Instructables page: https://www.instructables.com/Automated-Docking-Using-IR/

***

## Troubleshooting

- **No signal detected:**  
  - Confirm IR LED modulation using an oscilloscope or high-speed camera.  
  - Adjust `--threshold` lower if the signal is weak.  
- **False positives from ambient light:**  
  - Check filter cutoff and increase digital filter order.  
  - Add optical shields around receiver.  
- **Erratic bearing readings:**  
  - Increase sample rate or average over multiple readings.  
  - Ensure beacon alignment and stable mounting.  

***

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

[1] https://github.com/EvilChangIndia/IR-BasedAutoDockingRobot
