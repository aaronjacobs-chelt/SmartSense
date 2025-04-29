#!/usr/bin/env python3
"""
SmartSense Platform Demo

This script demonstrates the basic capabilities of the SmartSense IoT platform,
including sensor setup, data collection, alert configuration, and monitoring.
Use this as a starting point for your own SmartSense projects.

Usage:
    python examples/demo.py

Requirements:
    - SmartSense package installed
    - Python 3.9+
"""

import asyncio
import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional

# Add the project root to the Python path to import SmartSense
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import SmartSense components
from src.smartsense import SensorNetwork
from src.smartsense.sensors.base import (
    TemperatureSensor,
    HumiditySensor,
    PressureReading,
    TemperatureReading,
    HumidityReading,
)
from src.smartsense.utils.logging import configure_logging, get_logger

# Configure logging with a more verbose level for the demo
configure_logging(log_level="INFO", console=True)
logger = get_logger(__name__)


def print_sensor_reading(reading, prefix=""):
    """Print a sensor reading in a human-readable format."""
    timestamp = reading.timestamp.strftime("%H:%M:%S")
    
    if isinstance(reading, TemperatureReading):
        print(f"{prefix}[{timestamp}] Temperature: {reading.temperature:.1f}°{reading.unit}")
        if reading.unit == "C":
            print(f"{prefix}             {reading.to_fahrenheit():.1f}°F")
    
    elif isinstance(reading, HumidityReading):
        print(f"{prefix}[{timestamp}] Humidity: {reading.humidity:.1f}%")
    
    elif isinstance(reading, PressureReading):
        print(f"{prefix}[{timestamp}] Pressure: {reading.pressure:.1f} {reading.unit}")
    
    else:
        # Generic handling for other sensor types
        print(f"{prefix}[{timestamp}] Reading: {reading}")


def setup_demo_sensors() -> Dict[str, dict]:
    """
    Create configuration for demo sensors.
    
    These sensors are virtual and simulate real hardware for demonstration purposes.
    In a real deployment, you would configure actual hardware sensors.
    
    Returns:
        Dict[str, dict]: Dictionary of sensor configurations
    """
    return {
        "living_room_temp": {
            "name": "Living Room Temperature",
            "class": TemperatureSensor,
            "params": {
                "update_interval": 2.0,
                "min_value": 18.0,
                "max_value": 26.0,
                "noise_level": 0.2,
            }
        },
        "outdoor_temp": {
            "name": "Outdoor Temperature",
            "class": TemperatureSensor,
            "params": {
                "update_interval": 5.0,
                "min_value": 10.0,
                "max_value": 35.0,
                "noise_level": 0.5,
            }
        },
        "living_room_humidity": {
            "name": "Living Room Humidity",
            "class": HumiditySensor,
            "params": {
                "update_interval": 3.0,
                "min_value": 30.0,
                "max_value": 60.0,
                "noise_level": 0.8,
            }
        },
    }


def temperature_alert_action():
    """Action to execute when temperature alert is triggered."""
    print("\n🔥 ALERT: Temperature exceeds threshold! Activating cooling system...\n")


def humidity_alert_action():
    """Action to execute when humidity alert is triggered."""
    print("\n💧 ALERT: Humidity exceeds threshold! Activating dehumidifier...\n")


async def monitor_sensors(network: SensorNetwork, duration_seconds: int = 60):
    """
    Monitor sensors for a specified duration.
    
    Args:
        network: The sensor network to monitor
        duration_seconds: How long to run the monitoring loop (in seconds)
    """
    print("\n===== Starting Sensor Monitoring =====\n")
    
    # Start time for duration tracking
    start_time = time.time()
    end_time = start_time + duration_seconds
    
    try:
        while time.time() < end_time:
            # Clear the screen for better visibility (comment out if you prefer scrolling output)
            # os.system('cls' if os.name == 'nt' else 'clear')
            
            print(f"\n----- Sensor Readings at {datetime.now().strftime('%H:%M:%S')} -----")
            
            # Print the latest reading from each sensor
            for sensor_id, sensor in network.sensors.items():
                reading = sensor.get_last_reading()
                if reading:
                    print(f"\nSensor: {sensor.name}")
                    print_sensor_reading(reading, prefix="  ")
            
            # Sleep for a short period before the next update
            await asyncio.sleep(1.0)
            
            # Print a separator for clarity
            print("\n" + "-" * 50)
    
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    finally:
        # Ensure we stop the network when done
        print("\n===== Monitoring Complete =====")


async def main():
    """Main demo function."""
    print("Welcome to the SmartSense Platform Demo!")
    print("=======================================\n")
    
    # Step 1: Create a sensor network
    print("Step 1: Creating sensor network...")
    network = SensorNetwork(name="Demo Home Network", update_interval=1.0)
    
    # Step 2: Set up sensors
    print("Step 2: Setting up virtual sensors...")
    sensor_configs = setup_demo_sensors()
    
    for sensor_id, config in sensor_configs.items():
        # Create the sensor instance from configuration
        sensor_class = config["class"]
        sensor = sensor_class(
            name=config["name"],
            **config["params"]
        )
        
        # Add the sensor to the network
        network.add_sensor(sensor)
        print(f"  - Added sensor: {sensor.name} ({sensor.type})")
    
    # Step 3: Configure alerts
    print("\nStep 3: Configuring alerts...")
    
    # Temperature alert for living room
    temp_sensor_id = next(sensor_id for sensor_id, sensor in network.sensors.items() 
                         if "Living Room Temperature" == sensor.name)
    
    temp_alert_id = network.add_alert(
        sensor_id=temp_sensor_id,
        field="temperature",
        operator="gt",  # greater than
        value=25.0,     # 25°C threshold
        actions=[("activate_cooling", temperature_alert_action)],
        alert_name="High Temperature Alert",
        cooldown=10  # Wait 10 seconds between alerts
    )
    print(f"  - Added temperature alert with threshold 25°C")
    
    # Humidity alert for living room
    humidity_sensor_id = next(sensor_id for sensor_id, sensor in network.sensors.items() 
                             if "Living Room Humidity" == sensor.name)
    
    humidity_alert_id = network.add_alert(
        sensor_id=humidity_sensor_id,
        field="humidity",
        operator="gt",  # greater than
        value=55.0,     # 55% threshold
        actions=[("activate_dehumidifier", humidity_alert_action)],
        alert_name="High Humidity Alert",
        cooldown=10  # Wait 10 seconds between alerts
    )
    print(f"  - Added humidity alert with threshold 55%")
    
    # Step 4: Start the network
    print("\nStep 4: Starting the sensor network...")
    network.running = True
    
    # Initialize all sensors
    for sensor_id, sensor in network.sensors.items():
        await sensor.initialize()
        # Take an initial reading
        await sensor.read()
    
    # Step 5: Monitor sensors
    try:
        # Run monitoring for 60 seconds (adjust as needed)
        await monitor_sensors(network, duration_seconds=60)
    finally:
        # Ensure we clean up
        network.running = False
        print("Network stopped.")


if __name__ == "__main__":
    # Run the demo
    asyncio.run(main())

