# SmartSense 🌐

![SmartSense Logo](docs/images/logo.png) <!-- You'll need to add this image file later -->

[![Build Status](https://github.com/aaronjacobs-chelt/SmartSense/workflows/CI/badge.svg)](https://github.com/aaronjacobs-chelt/SmartSense/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Documentation Status](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://aaronjacobs-chelt.github.io/SmartSense/)

**SmartSense** is a cutting-edge IoT environmental monitoring and automation platform designed for modern distributed sensor networks. It combines real-time data collection, sophisticated analysis algorithms, and intuitive visualization tools to deliver actionable insights from your environment.

## 🚀 Features

- **Modern Microservices Architecture**: Built on a scalable, containerized architecture with Kubernetes support
- **Real-time Monitoring**: Low-latency data acquisition with sub-second response times
- **Extensible Sensor Framework**: Plug-and-play support for hundreds of sensors via modular adapters
- **Advanced Data Visualization**: Interactive dashboards powered by D3.js and Plotly
- **Comprehensive REST API**: Well-documented OpenAPI-compliant endpoints
- **Machine Learning Integration**: Anomaly detection and predictive maintenance
- **Automated CI/CD Pipeline**: Continuous testing and deployment with GitHub Actions
- **Cross-platform Support**: Runs on Linux, macOS, Windows, and various SBCs (Raspberry Pi, etc.)

## 📊 Dashboard Preview

![Dashboard Preview](docs/images/dashboard_preview.png) <!-- You'll need to add this image file later -->

## 🔧 Installation

SmartSense requires Python 3.9+ and can be installed via pip:

```bash
pip install smartsense
```

For development installation:

```bash
git clone https://github.com/aaronjacobs-chelt/SmartSense.git
cd SmartSense
pip install -e ".[dev]"
```

## 🔍 Quick Start

Here's a simple example to get you started with SmartSense:

```python
from smartsense import SensorNetwork
from smartsense.sensors.base import TemperatureSensor, HumiditySensor

# Create a sensor network
network = SensorNetwork(name="Home Environment")

# Add some sensors
network.add_sensor(TemperatureSensor(
    name="Living Room Temperature",
    update_interval=2.0,
    min_value=18.0,
    max_value=26.0,
))

network.add_sensor(HumiditySensor(
    name="Living Room Humidity",
    update_interval=3.0,
    min_value=30.0,
    max_value=60.0,
))

# Configure an alert
network.add_alert(
    sensor_id="temperature_abc123",  # Use the actual sensor ID
    field="temperature",
    operator="gt",                   # greater than
    value=25.0,                      # 25°C threshold
    actions=[("activate_cooling", lambda: print("Cooling activated!"))],
    alert_name="High Temperature Alert",
)

# Start the network
network.running = True

# In a real application, you would run the network in the background
# See examples/demo.py for a complete example
```

For a more comprehensive example, check out [examples/demo.py](examples/demo.py).

## 🏗️ Project Structure

```
SmartSense/
├── docs/               # Documentation
├── examples/           # Example scripts
├── src/                # Source code
│   └── smartsense/     # Main package
│       ├── api/        # REST API implementation
│       ├── core/       # Core monitoring system
│       ├── sensors/    # Sensor implementations
│       └── utils/      # Utility functions
├── tests/              # Test suite
└── ...
```

## 🔌 Supported Sensors

SmartSense supports a wide range of sensors, including:

### Environmental Sensors
- Temperature & Humidity (DHT11, DHT22, BME280)
- Pressure (BMP180, BMP280, BME680)
- Light (TSL2561, BH1750)
- Air Quality (MQ-135, CCS811, SGP30)

### Motion & Presence
- PIR Motion (HC-SR501)
- Ultrasonic Distance (HC-SR04)
- Infrared Proximity

### Water & Soil
- Water Level Sensors
- Flow Meters
- Soil Moisture
- pH Sensors

### Custom Sensors
SmartSense provides an extensible framework for adding custom sensor types by subclassing the `Sensor` base class.

## 🧠 Architecture

SmartSense is built on a modular, event-driven architecture that allows for flexible deployment options:

- **Core Monitoring System**: Central nervous system that manages sensor connections, data collection, and event processing
- **Sensor Abstraction Layer**: Provides a unified interface for different sensor types and hardware
- **Alert System**: Configurable alert conditions and actions based on sensor data
- **REST API**: HTTP-based interface for external integration
- **Data Storage**: Pluggable storage backends for sensor readings and configuration

## 🛠️ Extending SmartSense

SmartSense is designed to be easily extensible:

### Adding New Sensor Types

```python
from smartsense.sensors.base import Sensor, SensorReading
from typing import Optional

class MyCustomReading(SensorReading):
    value: float
    unit: str = "units"

class MyCustomSensor(Sensor):
    async def initialize(self) -> bool:
        # Initialize hardware or connections
        self._initialized = True
        return True
    
    async def read(self) -> Optional[SensorReading]:
        # Read data from the sensor
        value = 42.0  # Replace with actual reading
        
        reading = MyCustomReading(
            sensor_id=self.id,
            value=value
        )
        
        self._last_reading = reading
        self._last_read_time = time.time()
        
        return reading
```

### Creating Custom Alert Actions

```python
def my_custom_alert_action():
    # Custom action when alert is triggered
    print("Alert triggered! Taking action...")
    # Control hardware, send notification, etc.

# Add to a sensor network
network.add_alert(
    sensor_id="my_sensor_id",
    field="value",
    operator="gt",
    value=threshold_value,
    actions=[("my_custom_action", my_custom_alert_action)],
)
```

## 📝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report bugs**: Create a detailed issue with steps to reproduce
2. **Suggest features**: Open an issue to discuss your idea
3. **Submit pull requests**: Fork the repository and create a pull request with your changes

Please read our [Contributing Guidelines](CONTRIBUTING.md) before getting started.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/aaronjacobs-chelt/SmartSense.git

# Navigate to the directory
cd SmartSense

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## 📄 License

SmartSense is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- The amazing open-source community
- All [contributors](https://github.com/aaronjacobs-chelt/SmartSense/graphs/contributors)
- The [FastAPI](https://fastapi.tiangolo.com/) and [PyTorch](https://pytorch.org/) teams

---

Made with ❤️ by Aaron Jacobs

# SmartSense 🌐

![SmartSense Logo](docs/images/logo.png) <!-- You'll need to add this image file later -->

[![Build Status](https://github.com/aaronjacobs-chelt/SmartSense/workflows/CI/badge.svg)](https://github.com/aaronjacobs-chelt/SmartSense/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Documentation Status](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://aaronjacobs-chelt.github.io/SmartSense/)

**SmartSense** is a cutting-edge IoT environmental monitoring and automation platform designed for modern distributed sensor networks. It combines real-time data collection, sophisticated analysis algorithms, and intuitive visualization tools to deliver actionable insights from your environment.

## 🚀 Features

- **Modern Microservices Architecture**: Built on a scalable, containerized architecture with Kubernetes support
- **Real-time Monitoring**: Low-latency data acquisition with sub-second response times
- **Extensible Sensor Framework**: Plug-and-play support for hundreds of sensors via modular adapters
- **Advanced Data Visualization**: Interactive dashboards powered by D3.js and Plotly
- **Comprehensive REST API**: Well-documented OpenAPI-compliant endpoints
- **Machine Learning Integration**: Anomaly detection and predictive maintenance
- **Automated CI/CD Pipeline**: Continuous testing and deployment with GitHub Actions
- **Cross-platform Support**: Runs on Linux, macOS, Windows, and various SBCs (Raspberry Pi, etc.)

## 📊 Dashboard Preview

![Dashboard Preview](docs/images/dashboard_preview.png) <!-- You'll need to add this image file later -->

## 🔧 Installation

SmartSense requires Python 3.9+ and can be installed via pip:

```bash
pip install smartsense
```

For development installation:

```bash
git clone https://github.com/aaronjacobs-chelt/SmartSense.git
cd SmartSense
pip install -e ".[dev]"
```

See [Getting Started](docs/getting_started.md) for complete installation instructions.

## 🔍 Quick Start

```python
from smartsense import SensorNetwork, sensors

# Initialize the network
network = SensorNetwork()

# Add sensors
network.add_sensor(sensors.TemperatureSensor(pin=4))
network.add_sensor(sensors.HumiditySensor(pin=17))

# Start monitoring
network.start()

# Access real-time data
current_temp = network.get_sensor_data('temperature')
print(f"Current temperature: {current_temp}°C")

# Set up alerts
network.add_alert('temperature', threshold=30, action=lambda: print("Temperature alert!"))
```

## 📘 Documentation

Comprehensive documentation is available at [aaronjacobs-chelt.github.io/SmartSense](https://aaronjacobs-chelt.github.io/SmartSense/).

- [API Reference](docs/api_reference.md)
- [Sensor Configuration](docs/sensor_configuration.md)
- [Dashboard Setup](docs/dashboard_setup.md)
- [Automation Rules](docs/automation_rules.md)
- [Advanced Topics](docs/advanced_topics.md)

## 🔌 Supported Sensors

SmartSense supports a wide range of sensors, including:

- Temperature & Humidity (DHT11, DHT22, BME280)
- Pressure (BMP180, BMP280, BME680)
- Light (TSL2561, BH1750)
- Air Quality (MQ-135, CCS811, SGP30)
- Motion (PIR HC-SR501, ultrasonic HC-SR04)
- Water (level sensors, flow meters, pH sensors)
- And many more!

Custom sensor support can be added through the extensible adapter framework.

## 🛠️ Contributing

Contributions are welcome! Please check out our [contribution guidelines](CONTRIBUTING.md) before getting started.

## 📝 License

SmartSense is open-source software licensed under the [MIT license](LICENSE).

## 🙏 Acknowledgments

- The amazing open-source community
- All our [contributors](https://github.com/aaronjacobs-chelt/SmartSense/graphs/contributors)
- The [FastAPI](https://fastapi.tiangolo.com/) and [PyTorch](https://pytorch.org/) teams

