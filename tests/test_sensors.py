"""
Tests for the SmartSense sensor implementation.

This module contains unit tests for the sensor classes and utilities
in the SmartSense platform, including base sensor functionality,
virtual sensors, and specific sensor types.
"""

import asyncio
import pytest
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union

import pytest

from smartsense.sensors.base import (
    HumidityReading,
    HumiditySensor,
    LightReading,
    PressureReading,
    Sensor,
    SensorReading,
    TemperatureReading,
    TemperatureSensor,
    VirtualSensor,
)


# -- Test fixtures --

@pytest.fixture
def virtual_sensor():
    """Create a generic virtual sensor for testing."""
    sensor = VirtualSensor(
        name="Test Sensor",
        sensor_type="test",
        update_interval=0.1,
        min_value=10.0,
        max_value=20.0,
        noise_level=0.5,
    )
    return sensor


@pytest.fixture
def temperature_sensor():
    """Create a virtual temperature sensor for testing."""
    sensor = TemperatureSensor(
        name="Test Temperature",
        update_interval=0.1,
        min_value=15.0,
        max_value=30.0,
        noise_level=0.2,
        pin=4,
    )
    return sensor


@pytest.fixture
def humidity_sensor():
    """Create a virtual humidity sensor for testing."""
    sensor = HumiditySensor(
        name="Test Humidity",
        update_interval=0.1,
        min_value=40.0,
        max_value=60.0,
        noise_level=0.5,
        pin=17,
    )
    return sensor


# -- Base Sensor Reading Tests --

def test_sensor_reading_creation():
    """Test creating a basic sensor reading."""
    reading = SensorReading(sensor_id="test_sensor_1")
    
    assert reading.sensor_id == "test_sensor_1"
    assert isinstance(reading.timestamp, datetime)
    
    # Test automatic timestamp generation
    now = datetime.now()
    assert now - timedelta(seconds=1) <= reading.timestamp <= now + timedelta(seconds=1)


def test_temperature_reading():
    """Test temperature reading and unit conversions."""
    # Test Celsius reading
    c_reading = TemperatureReading(
        sensor_id="temp_1",
        temperature=25.0,
        unit="C",
    )
    
    assert c_reading.temperature == 25.0
    assert c_reading.unit == "C"
    assert c_reading.to_fahrenheit() == pytest.approx(77.0)
    assert c_reading.to_celsius() == 25.0
    
    # Test Fahrenheit reading
    f_reading = TemperatureReading(
        sensor_id="temp_1",
        temperature=77.0,
        unit="F",
    )
    
    assert f_reading.temperature == 77.0
    assert f_reading.unit == "F"
    assert f_reading.to_celsius() == pytest.approx(25.0)
    assert f_reading.to_fahrenheit() == 77.0


def test_humidity_reading_validation():
    """Test humidity reading creation and validation."""
    # Valid humidity
    valid_reading = HumidityReading(
        sensor_id="humidity_1",
        humidity=50.0,
    )
    assert valid_reading.humidity == 50.0
    
    # Test validation error for out-of-bounds humidity
    with pytest.raises(ValueError):
        HumidityReading(
            sensor_id="humidity_1",
            humidity=101.0,  # Over 100%
        )
    
    with pytest.raises(ValueError):
        HumidityReading(
            sensor_id="humidity_1",
            humidity=-1.0,  # Below 0%
        )


def test_pressure_reading_conversions():
    """Test pressure reading and unit conversions."""
    # Test hPa reading
    hpa_reading = PressureReading(
        sensor_id="pressure_1",
        pressure=1013.25,
        unit="hPa",
    )
    
    assert hpa_reading.pressure == 1013.25
    assert hpa_reading.unit == "hPa"
    assert hpa_reading.to_inhg() == pytest.approx(29.921, abs=0.001)
    assert hpa_reading.to_hpa() == 1013.25
    
    # Test inHg reading
    inhg_reading = PressureReading(
        sensor_id="pressure_1",
        pressure=29.92,
        unit="inHg",
    )
    
    assert inhg_reading.pressure == 29.92
    assert inhg_reading.unit == "inHg"
    assert inhg_reading.to_hpa() == pytest.approx(1013.21, abs=0.1)
    assert inhg_reading.to_inhg() == 29.92


def test_light_reading():
    """Test light reading creation."""
    reading = LightReading(
        sensor_id="light_1",
        light_level=500.0,
    )
    
    assert reading.light_level == 500.0
    assert reading.unit == "lux"


# -- Virtual Sensor Tests --

def test_virtual_sensor_initialization(virtual_sensor):
    """Test virtual sensor initialization."""
    assert virtual_sensor.name == "Test Sensor"
    assert virtual_sensor.type == "test"
    assert virtual_sensor.update_interval == 0.1
    assert virtual_sensor.min_value == 10.0
    assert virtual_sensor.max_value == 20.0
    assert virtual_sensor.noise_level == 0.5
    assert virtual_sensor._initialized is False
    
    # Check ID generation
    assert virtual_sensor.id.startswith("test_")
    assert len(virtual_sensor.id) > 5


@pytest.mark.asyncio
async def test_virtual_sensor_initialize(virtual_sensor):
    """Test asynchronous initialization of a virtual sensor."""
    assert virtual_sensor._initialized is False
    
    result = await virtual_sensor.initialize()
    
    assert result is True
    assert virtual_sensor._initialized is True


@pytest.mark.asyncio
async def test_virtual_sensor_reading(virtual_sensor):
    """Test getting readings from a virtual sensor."""
    # Initialize the sensor
    await virtual_sensor.initialize()
    
    # Get a reading
    reading = await virtual_sensor.read()
    
    # Verify reading properties
    assert reading is not None
    assert reading.sensor_id == virtual_sensor.id
    assert hasattr(reading, "value")
    assert virtual_sensor.min_value <= reading.value <= virtual_sensor.max_value
    
    # Verify sensor state was updated
    assert virtual_sensor._last_reading == reading
    assert virtual_sensor._last_read_time is not None


def test_virtual_sensor_read_sync(virtual_sensor):
    """Test synchronous reading from a virtual sensor."""
    reading = virtual_sensor.read_sync()
    
    assert reading is not None
    assert reading.sensor_id == virtual_sensor.id
    assert hasattr(reading, "value")
    assert virtual_sensor.min_value <= reading.value <= virtual_sensor.max_value


@pytest.mark.asyncio
async def test_virtual_sensor_multiple_readings(virtual_sensor):
    """Test getting multiple readings from a virtual sensor."""
    readings = []
    for _ in range(5):
        reading = await virtual_sensor.read()
        readings.append(reading)
        # Use a small delay to allow for value drift
        await asyncio.sleep(0.01)
    
    # Verify we have 5 readings
    assert len(readings) == 5
    
    # Values should be in the valid range and show some variation
    values = [r.value for r in readings]
    assert all(virtual_sensor.min_value <= v <= virtual_sensor.max_value for v in values)
    
    # Check if values are not all identical (this test could theoretically fail
    # if by random chance all readings happen to be identical, but unlikely)
    assert len(set(values)) > 1, "Expected some variation in sensor readings"


# -- Specific Sensor Type Tests --

@pytest.mark.asyncio
async def test_temperature_sensor_reading(temperature_sensor):
    """Test getting readings from a temperature sensor."""
    # Initialize the sensor
    await temperature_sensor.initialize()
    
    # Get a reading
    reading = await temperature_sensor.read()
    
    # Verify reading properties
    assert reading is not None
    assert reading.sensor_id == temperature_sensor.id
    assert hasattr(reading, "temperature")
    assert temperature_sensor.min_value <= reading.temperature <= temperature_sensor.max_value
    assert reading.unit == "C"
    
    # Verify sensor state was updated
    assert temperature_sensor._last_reading == reading
    assert temperature_sensor._last_read_time is not None
    
    # Test getting metadata
    metadata = temperature_sensor.get_metadata()
    assert metadata["name"] == "Test Temperature"
    assert metadata["type"] == "temperature"
    assert metadata["pin"] == 4
    assert metadata["last_read_time"] is not None


@pytest.mark.asyncio
async def test_humidity_sensor_reading(humidity_sensor):
    """Test getting readings from a humidity sensor."""
    # Initialize the sensor
    await humidity_sensor.initialize()
    
    # Get a reading
    reading = await humidity_sensor.read()
    
    # Verify reading properties
    assert reading is not None
    assert reading.sensor_id == humidity_sensor.id
    assert hasattr(reading, "humidity")
    assert humidity_sensor.min_value <= reading.humidity <= humidity_sensor.max_value
    
    # Verify humidity is in valid range
    assert 0 <= reading.humidity <= 100
    
    # Test humidity validation - this shouldn't happen with a properly
    # implemented sensor, but let's verify the validation works
    with pytest.raises(ValueError):
        HumidityReading(
            sensor_id=humidity_sensor.id,
            humidity=101.0,  # Invalid humidity
        )


# -- Error Handling Tests --

class BrokenSensor(Sensor):
    """A sensor implementation that raises exceptions for testing error handling."""
    
    async def initialize(self) -> bool:
        """Initialization that fails."""
        raise RuntimeError("Simulated initialization failure")
    
    async def read(self) -> Optional[SensorReading]:
        """Reading that fails."""
        raise RuntimeError("Simulated reading failure")


@pytest.mark.asyncio
async def test_sensor_error_handling():
    """Test error handling in sensors."""
    sensor = BrokenSensor(name="Broken Sensor", sensor_type="broken")
    
    # Test initialization error handling
    with pytest.raises(RuntimeError):
        await sensor.initialize()
    
    # Test reading error handling
    with pytest.raises(RuntimeError):
        await sensor.read()
    
    # Test synchronous reading error handling
    with pytest.raises(RuntimeError):
        sensor.read_sync()


if __name__ == "__main__":
    pytest.main(["-v", __file__])

