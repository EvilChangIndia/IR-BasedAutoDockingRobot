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

6. [License](#license)  

***

## Features

- **Ambient-Light Immunity:** Hardware adjusts for ambient light.
- **Beacon Signal Strength Variation Compensation:** Adaptive thresholding circuitry handles fluctuations in received signal strength.  
- **Python Core:** Simple scripts for beacon testing and docking logic—easily extended or embedded.  

***

## Directory Structure

```plaintext
IR-BasedAutoDockingRobot/
├── beacon_test.py       # Test script to verify IR beacon reception
├── auto_docker.py       # Main docking routine (no motor control)
├── main.py              # Main program for the robot with motor control
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
3. Check https://www.instructables.com/Automated-Docking-Using-IR/ 

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




## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

[1] https://github.com/EvilChangIndia/IR-BasedAutoDockingRobot
