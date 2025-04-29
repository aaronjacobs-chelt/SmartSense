"""
SmartSense - A sophisticated IoT environmental monitoring and automation platform.

This package provides a comprehensive framework for connecting, monitoring, and
automating IoT devices and environmental sensors. It includes real-time data
collection, analysis, visualization, and control capabilities.
"""

__version__ = "0.1.0"

from smartsense.core.monitor import SensorNetwork
from smartsense.sensors.base import Sensor, SensorReading

__all__ = ["SensorNetwork", "Sensor", "SensorReading"]

