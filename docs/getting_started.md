# Getting Started with SmartSense

This guide will walk you through the process of setting up SmartSense, connecting your first sensors, and creating a basic monitoring dashboard.

## Prerequisites

Before installing SmartSense, ensure you have the following:

- Python 3.9 or higher
- pip (Python package installer)
- Git (for development installation)
- Access to GPIO pins (if using hardware sensors)

### Supported Platforms

SmartSense runs on:

- Linux (Ubuntu, Debian, Raspberry Pi OS, etc.)
- macOS 10.14+
- Windows 10/11
- Raspberry Pi (all models)
- Other SBCs (Jetson Nano, Orange Pi, etc.)

## Installation Options

### 1. Standard Installation

For most users, the standard installation via pip is recommended:

```bash
pip install smartsense
```

### 2. Development Installation

For contributors or those who want the latest features:

```bash
git clone https://github.com/aaronjacobs-chelt/SmartSense.git
cd SmartSense
pip install -e ".[dev]"
```

### 3. Docker Installation

For containerized deployment:

```bash
docker pull aaronjacobs/smartsense:latest
docker run -p 8000:8000 -p 8050:8050 aaronjacobs/smartsense
```

## Configuration

SmartSense uses a YAML configuration file. Create a file named `config.yml` in your project directory:

```yaml
network:
  name: "Home Environment Monitoring"
  update_interval: 5  # seconds

sensors:
  - type: "temperature"
    name: "Living Room Temperature"
    pin: 4
    model: "DHT22"
    
  - type: "humidity"
    name: "Living Room Humidity"
    pin: 4
    model: "DHT22"
    
  - type: "light"
    name: "Ambient Light"
    pin: 17
    model: "BH1750"

alerts:
  - sensor: "Living Room Temperature"
    condition: "above"
    threshold: 28
    actions:
      - "notify_email"
      - "activate_fan"
```

## Connecting Your First Sensor

### Hardware Connection

For a basic temperature and humidity setup with a DHT22 sensor:

1. Connect the DHT22 VCC pin to 3.3V on your board
2. Connect the DHT22 GND pin to ground on your board
3. Connect the DHT22 DATA pin to GPIO4 on your board
4. Add a 10K ohm pull-up resistor between VCC and DATA pins

![DHT22 Connection Diagram](images/dht22_wiring.png) <!-- You'll need to add this image file later -->

### Software Setup

Initialize your first sensor network:

```python
from smartsense import SensorNetwork, sensors

# Create a network
network = SensorNetwork(name="Home Monitor")

# Add a temperature/humidity sensor
dht22 = sensors.DHT22Sensor(
    name="Living Room Climate",
    pin=4
)
network.add_sensor(dht22)

# Start monitoring
network.start()

# Display current readings
print(f"Temperature: {dht22.temperature}°C")
print(f"Humidity: {dht22.humidity}%")
```

## Launching the Dashboard

SmartSense includes a web-based dashboard for data visualization:

```bash
smartsense-dashboard --config config.yml
```

This will start the dashboard on http://localhost:8050

## Setting Up Automations

Create automated responses to sensor conditions:

```python
from smartsense import SensorNetwork, sensors, actions

network = SensorNetwork()
temp_sensor = sensors.TemperatureSensor(pin=4)
fan_control = actions.RelayControl(pin=18)

network.add_sensor(temp_sensor)

# Create an automation rule
network.add_automation(
    condition=lambda: temp_sensor.value > 25,
    action=lambda: fan_control.activate(),
    reset=lambda: temp_sensor.value < 23,
    reset_action=lambda: fan_control.deactivate()
)

network.start()
```

## Next Steps

Now that you have SmartSense up and running, you might want to explore:

- [Adding more sensor types](sensor_configuration.md)
- [Creating custom dashboards](dashboard_setup.md)
- [Setting up the REST API](api_setup.md)
- [Integrating with other systems](integrations.md)
- [Advanced automation rules](automation_rules.md)

## Troubleshooting

If you encounter issues during setup:

1. Check your hardware connections
2. Verify your GPIO pin numbers
3. Ensure you have the required permissions to access GPIO pins
4. Consult the [Troubleshooting Guide](troubleshooting.md)
5. Search existing [GitHub Issues](https://github.com/aaronjacobs-chelt/SmartSense/issues)

If your issue persists, please [open a new GitHub issue](https://github.com/aaronjacobs-chelt/SmartSense/issues/new) with details about your setup and the problem you're experiencing.

