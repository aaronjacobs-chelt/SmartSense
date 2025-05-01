# API Reference

## Version: 1.0.0 (May 2025)

Complete API documentation for SmartSense modules and classes.

## Core Modules

- [Monitor](core/monitor.md) - Core monitoring system
- [Sensors](sensors/index.md) - Sensor implementations
- [API](api/routes.md) - REST API endpoints
- [Utils](utils/index.md) - Utility functions

## Quick Links

- [Getting Started](../getting_started.md)
- [Examples](../../examples/)
- [Configuration Guide](../sensor_configuration.md)

## Module Index

### smartsense.core

Core functionality for sensor network management.

```python
from smartsense import SensorNetwork
network = SensorNetwork(name="My Network")
```

### smartsense.sensors

Sensor implementations and base classes.

```python
from smartsense.sensors import TemperatureSensor
sensor = TemperatureSensor(name="Room Temp")
```

### smartsense.api

REST API implementation.

```python
from smartsense.api import create_app
app = create_app()
```

### smartsense.utils

Utility functions and helpers.

```python
from smartsense.utils import setup_logging
setup_logging(level="DEBUG")
```

## Class Hierarchy

- SensorNetwork
  - Sensor
    - TemperatureSensor
    - HumiditySensor
  - Alert
  - DataStore

## Further Reading

- [Architecture Overview](../architecture.md)
- [Development Guide](../../CONTRIBUTING.md)
- [Examples](../../examples/)

---

Last updated: May 1, 2025
