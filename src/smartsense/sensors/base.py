"""
Base sensor interface for SmartSense.

This module defines the base classes and interfaces for all sensor types in the
SmartSense platform. It provides abstract base classes and common functionality
that specific sensor implementations should extend.
"""

import abc
import asyncio
import time
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, TypeVar, Union, cast

from pydantic import BaseModel, Field, validator

from smartsense.utils.logging import get_logger

logger = get_logger(__name__)

# Type variable for sensor reading subclasses
T = TypeVar('T', bound='SensorReading')


class SensorReading(BaseModel):
    """Base model for sensor readings."""
    
    timestamp: datetime = Field(default_factory=datetime.now)
    sensor_id: str
    
    class Config:
        """Pydantic model configuration."""
        
        arbitrary_types_allowed = True
        extra = "allow"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert reading to a dictionary."""
        return self.dict()
    
    @validator('timestamp', pre=True, always=True)
    def set_timestamp(cls, v: Any) -> datetime:
        """Set timestamp to current time if not provided."""
        if v is None:
            return datetime.now()
        return v


class TemperatureReading(SensorReading):
    """Temperature sensor reading."""
    
    temperature: float
    unit: str = "C"  # Celsius by default
    
    def to_fahrenheit(self) -> float:
        """Convert temperature to Fahrenheit if in Celsius."""
        if self.unit == "C":
            return (self.temperature * 9/5) + 32
        return self.temperature
    
    def to_celsius(self) -> float:
        """Convert temperature to Celsius if in Fahrenheit."""
        if self.unit == "F":
            return (self.temperature - 32) * 5/9
        return self.temperature


class HumidityReading(SensorReading):
    """Humidity sensor reading."""
    
    humidity: float  # Relative humidity percentage (0-100)
    
    @validator('humidity')
    def validate_humidity(cls, v: float) -> float:
        """Validate humidity is within reasonable bounds."""
        if not 0 <= v <= 100:
            raise ValueError(f"Humidity must be between 0 and 100%, got {v}%")
        return v


class PressureReading(SensorReading):
    """Atmospheric pressure sensor reading."""
    
    pressure: float  # Pressure in hPa (hectopascals)
    unit: str = "hPa"
    
    def to_inhg(self) -> float:
        """Convert pressure to inches of mercury."""
        if self.unit == "hPa":
            return self.pressure * 0.02953
        return self.pressure
    
    def to_hpa(self) -> float:
        """Convert pressure to hectopascals."""
        if self.unit == "inHg":
            return self.pressure / 0.02953
        return self.pressure


class LightReading(SensorReading):
    """Light level sensor reading."""
    
    light_level: float  # Light level in lux
    unit: str = "lux"


class Sensor(abc.ABC):
    """
    Abstract base class for all sensors.
    
    This class defines the interface that all sensor implementations must follow.
    It provides common functionality and ensures consistent behavior across
    different sensor types.
    """
    
    def __init__(
        self,
        name: str,
        sensor_type: str,
        update_interval: float = 1.0,
        pin: Optional[int] = None,
        sensor_id: Optional[str] = None,
    ):
        """
        Initialize a sensor.
        
        Args:
            name: Human-readable name for this sensor
            sensor_type: Type identifier for this sensor
            update_interval: How often to poll this sensor (in seconds)
            pin: GPIO pin number (if applicable)
            sensor_id: Unique ID for this sensor (generated if not provided)
        """
        self.name = name
        self.type = sensor_type
        self.update_interval = update_interval
        self.pin = pin
        self.id = sensor_id or f"{sensor_type}_{str(uuid.uuid4())[:8]}"
        self._initialized = False
        self._last_reading: Optional[SensorReading] = None
        self._last_read_time: Optional[float] = None
        
        logger.info(f"Created {sensor_type} sensor: {name} (ID: {self.id})")
    
    def __repr__(self) -> str:
        """Return string representation of the sensor."""
        return f"<{self.__class__.__name__} name='{self.name}' id='{self.id}'>"
    
    @abc.abstractmethod
    async def initialize(self) -> bool:
        """
        Initialize the sensor hardware or connection.
        
        This method should be implemented by subclasses to handle any
        initialization logic specific to the sensor type.
        
        Returns:
            bool: True if initialization was successful, False otherwise
        """
        pass
    
    @abc.abstractmethod
    async def read(self) -> Optional[SensorReading]:
        """
        Read data from the sensor.
        
        This method should be implemented by subclasses to handle the
        actual data acquisition from the sensor.
        
        Returns:
            Optional[SensorReading]: A sensor reading object if successful, None otherwise
        """
        pass
    
    def read_sync(self) -> Optional[SensorReading]:
        """
        Synchronous wrapper for the async read method.
        
        This method provides a synchronous interface to the asynchronous read
        method, which is useful for code that can't use async/await.
        
        Returns:
            Optional[SensorReading]: A sensor reading object if successful, None otherwise
        """
        # Use a new event loop in a separate thread for the synchronous call
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(self.read())
        finally:
            loop.close()
    
    async def close(self) -> None:
        """
        Clean up resources used by the sensor.
        
        This method should be called when the sensor is no longer needed
        to free up any resources it may be using.
        """
        logger.info(f"Closing sensor: {self.name} (ID: {self.id})")
    
    def get_last_reading(self) -> Optional[SensorReading]:
        """
        Get the most recent reading from this sensor.
        
        Returns:
            Optional[SensorReading]: The most recent reading, or None if no readings yet
        """
        return self._last_reading
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get metadata about this sensor.
        
        Returns:
            Dict[str, Any]: Sensor metadata
        """
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "update_interval": self.update_interval,
            "pin": self.pin,
            "last_read_time": self._last_read_time,
        }


class VirtualSensor(Sensor):
    """
    A virtual sensor that generates simulated data.
    
    This sensor type is useful for testing and development when
    physical hardware is not available.
    """
    
    def __init__(
        self,
        name: str,
        sensor_type: str = "virtual",
        update_interval: float = 1.0,
        min_value: float = 0.0,
        max_value: float = 100.0,
        noise_level: float = 1.0,
        reading_class: type = SensorReading,
        reading_field: str = "value",
    ):
        """
        Initialize a virtual sensor.
        
        Args:
            name: Human-readable name for this sensor
            sensor_type: Type identifier for this sensor
            update_interval: How often to poll this sensor (in seconds)
            min_value: Minimum value to generate
            max_value: Maximum value to generate
            noise_level: Amount of random noise to add
            reading_class: Class to use for readings
            reading_field: Field name for the generated value
        """
        super().__init__(name, sensor_type, update_interval)
        self.min_value = min_value
        self.max_value = max_value
        self.noise_level = noise_level
        self.reading_class = reading_class
        self.reading_field = reading_field
        self._current_value = (min_value + max_value) / 2
        
    async def initialize(self) -> bool:
        """Initialize the virtual sensor."""
        logger.debug(f"Initializing virtual sensor: {self.name}")
        self._initialized = True
        return True
    
    async def read(self) -> Optional[SensorReading]:
        """Generate a simulated sensor reading."""
        if not self._initialized:
            await self.initialize()
        
        # Update the simulated value with some noise and drift
        import random
        noise = random.uniform(-self.noise_level, self.noise_level)
        drift = random.uniform(-0.1, 0.1)
        
        self._current_value += noise + drift
        
        # Keep the value within bounds
        self._current_value = max(self.min_value, min(self._current_value, self.max_value))
        
        # Create a reading with the appropriate class
        data = {
            "sensor_id": self.id,
            self.reading_field: self._current_value
        }
        
        reading = self.reading_class(**data)
        
        # Update sensor state
        self._last_reading = reading
        self._last_read_time = time.time()
        
        return reading


class TemperatureSensor(VirtualSensor):
    """Virtual temperature sensor for testing."""
    
    def __init__(
        self,
        name: str = "Virtual Temperature",
        update_interval: float = 1.0,
        min_value: float = 15.0,
        max_value: float = 30.0,
        noise_level: float = 0.2,
        pin: Optional[int] = None,
    ):
        """Initialize a virtual temperature sensor."""
        super().__init__(
            name=name,
            sensor_type="temperature",
            update_interval=update_interval,
            min_value=min_value,
            max_value=max_value,
            noise_level=noise_level,
            reading_class=TemperatureReading,
            reading_field="temperature",
        )
        self.pin = pin


class HumiditySensor(VirtualSensor):
    """Virtual humidity sensor for testing."""
    
    def __init__(
        self,
        name: str = "Virtual Humidity",
        update_interval: float = 1.0,
        min_value: float = 30.0,
        max_value: float = 70.0,
        noise_level: float = 0.5,
        pin: Optional[int] = None,
    ):
        """Initialize a virtual humidity sensor."""
        super().__init__(
            name=name,
            sensor_type="humidity",
            update_interval=update_interval,
            min_value=min_value,
            max_value=max_value,
            noise_level=noise_level,
            reading_class=HumidityReading,
            reading_field="humidity",
        )
        self.pin = pin


# Utility functions for working with sensors
def create_sensor_from_config(config: Dict[str, Any]) -> Sensor:
    """
    Create a sensor from a configuration dictionary.
    
    Args:
        config: Sensor configuration dictionary
        
    Returns

"""
Base sensor interface for SmartSense.

This module defines the base classes and interfaces for all sensor types in the
SmartSense platform. It provides abstract base classes and common functionality
that specific sensor implementations should extend.
"""

import abc
import asyncio
import time
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, TypeVar, Union, cast

from pydantic import BaseModel, Field, validator

from smartsense.utils.logging import get_logger

logger = get_logger(__name__)

# Type variable for sensor reading subclasses
T = TypeVar('T', bound='SensorReading')


class SensorReading(BaseModel):
    """Base model for sensor readings."""
    
    timestamp: datetime = Field(default_factory=datetime.now)
    sensor_id: str
    
    class Config:
        """Pydantic model configuration."""
        
        arbitrary_types_allowed = True
        extra = "allow"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert reading to a dictionary."""
        return self.dict()
    
    @validator('timestamp', pre=True, always=True)
    def set_timestamp(cls, v: Any) -> datetime:
        """Set timestamp to current time if not provided."""
        if v is None:
            return datetime.now()
        return v


class TemperatureReading(SensorReading):
    """Temperature sensor reading."""
    
    temperature: float
    unit: str = "C"  # Celsius by default
    
    def to_fahrenheit(self) -> float:
        """Convert temperature to Fahrenheit if in Celsius."""
        if self.unit == "C":
            return (self.temperature * 9/5) + 32
        return self.temperature
    
    def to_celsius(self) -> float:
        """Convert temperature to Celsius if in Fahrenheit."""
        if self.unit == "F":
            return (self.temperature - 32) * 5/9
        return self.temperature


class HumidityReading(SensorReading):
    """Humidity sensor reading."""
    
    humidity: float  # Relative humidity percentage (0-100)
    
    @validator('humidity')
    def validate_humidity(cls, v: float) -> float:
        """Validate humidity is within reasonable bounds."""
        if not 0 <= v <= 100:
            raise ValueError(f"Humidity must be between 0 and 100%, got {v}%")
        return v


class PressureReading(SensorReading):
    """Atmospheric pressure sensor reading."""
    
    pressure: float  # Pressure in hPa (hectopascals)
    unit: str = "hPa"
    
    def to_inhg(self) -> float:
        """Convert pressure to inches of mercury."""
        if self.unit == "hPa":
            return self.pressure * 0.02953
        return self.pressure
    
    def to_hpa(self) -> float:
        """Convert pressure to hectopascals."""
        if self.unit == "inHg":
            return self.pressure / 0.02953
        return self.pressure


class LightReading(SensorReading):
    """Light level sensor reading."""
    
    light_level: float  # Light level in lux
    unit: str = "lux"


class Sensor(abc.ABC):
    """
    Abstract base class for all sensors.
    
    This class defines the interface that all sensor implementations must follow.
    It provides common functionality and ensures consistent behavior across
    different sensor types.
    """
    
    def __init__(
        self,
        name: str,
        sensor_type: str,
        update_interval: float = 1.0,
        pin: Optional[int] = None,
        sensor_id: Optional[str] = None,
    ):
        """
        Initialize a sensor.
        
        Args:
            name: Human-readable name for this sensor
            sensor_type: Type identifier for this sensor
            update_interval: How often to poll this sensor (in seconds)
            pin: GPIO pin number (if applicable)
            sensor_id: Unique ID for this sensor (generated if not provided)
        """
        self.name = name
        self.type = sensor_type
        self.update_interval = update_interval
        self.pin = pin
        self.id = sensor_id or f"{sensor_type}_{str(uuid.uuid4())[:8]}"
        self._initialized = False
        self._last_reading: Optional[SensorReading] = None
        self._last_read_time: Optional[float] = None
        
        logger.info(f"Created {sensor_type} sensor: {name} (ID: {self.id})")
    
    def __repr__(self) -> str:
        """Return string representation of the sensor."""
        return f"<{self.__class__.__name__} name='{self.name}' id='{self.id}'>"
    
    @abc.abstractmethod
    async def initialize(self) -> bool:
        """
        Initialize the sensor hardware or connection.
        
        This method should be implemented by subclasses to handle any
        initialization logic specific to the sensor type.
        
        Returns:
            bool: True if initialization was successful, False otherwise
        """
        pass
    
    @abc.abstractmethod
    async def read(self) -> Optional[SensorReading]:
        """
        Read data from the sensor.
        
        This method should be implemented by subclasses to handle the
        actual data acquisition from the sensor.
        
        Returns:
            Optional[SensorReading]: A sensor reading object if successful, None otherwise
        """
        pass
    
    def read_sync(self) -> Optional[SensorReading]:
        """
        Synchronous wrapper for the async read method.
        
        This method provides a synchronous interface to the asynchronous read
        method, which is useful for code that can't use async/await.
        
        Returns:
            Optional[SensorReading]: A sensor reading object if successful, None otherwise
        """
        # Use a new event loop in a separate thread for the synchronous call
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(self.read())
        finally:
            loop.close()
    
    async def close(self) -> None:
        """
        Clean up resources used by the sensor.
        
        This method should be called when the sensor is no longer needed
        to free up any resources it may be using.
        """
        logger.info(f"Closing sensor: {self.name} (ID: {self.id})")
    
    def get_last_reading(self) -> Optional[SensorReading]:
        """
        Get the most recent reading from this sensor.
        
        Returns:
            Optional[SensorReading]: The most recent reading, or None if no readings yet
        """
        return self._last_reading
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get metadata about this sensor.
        
        Returns:
            Dict[str, Any]: Sensor metadata
        """
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "update_interval": self.update_interval,
            "pin": self.pin,
            "last_read_time": self._last_read_time,
        }


class VirtualSensor(Sensor):
    """
    A virtual sensor that generates simulated data.
    
    This sensor type is useful for testing and development when
    physical hardware is not available.
    """
    
    def __init__(
        self,
        name: str,
        sensor_type: str = "virtual",
        update_interval: float = 1.0,
        min_value: float = 0.0,
        max_value: float = 100.0,
        noise_level: float = 1.0,
        reading_class: type = SensorReading,
        reading_field: str = "value",
    ):
        """
        Initialize a virtual sensor.
        
        Args:
            name: Human-readable name for this sensor
            sensor_type: Type identifier for this sensor
            update_interval: How often to poll this sensor (in seconds)
            min_value: Minimum value to generate
            max_value: Maximum value to generate
            noise_level: Amount of random noise to add
            reading_class: Class to use for readings
            reading_field: Field name for the generated value
        """
        super().__init__(name, sensor_type, update_interval)
        self.min_value = min_value
        self.max_value = max_value
        self.noise_level = noise_level
        self.reading_class = reading_class
        self.reading_field = reading_field
        self._current_value = (min_value + max_value) / 2
        
    async def initialize(self) -> bool:
        """Initialize the virtual sensor."""
        logger.debug(f"Initializing virtual sensor: {self.name}")
        self._initialized = True
        return True
    
    async def read(self) -> Optional[SensorReading]:
        """Generate a simulated sensor reading."""
        if not self._initialized:
            await self.initialize()
        
        # Update the simulated value with some noise and drift
        import random
        noise = random.uniform(-self.noise_level, self.noise_level)
        drift = random.uniform(-0.1, 0.1)
        
        self._current_value += noise + drift
        
        # Keep the value within bounds
        self._current_value = max(self.min_value, min(self._current_value, self.max_value))
        
        # Create a reading with the appropriate class
        data = {
            "sensor_id": self.id,
            self.reading_field: self._current_value
        }
        
        reading = self.reading_class(**data)
        
        # Update sensor state
        self._last_reading = reading
        self._last_read_time = time.time()
        
        return reading


class TemperatureSensor(VirtualSensor):
    """Virtual temperature sensor for testing."""
    
    def __init__(
        self,
        name: str = "Virtual Temperature",
        update_interval: float = 1.0,
        min_value: float = 15.0,
        max_value: float = 30.0,
        noise_level: float = 0.2,
        pin: Optional[int] = None,
    ):
        """Initialize a virtual temperature sensor."""
        super().__init__(
            name=name,
            sensor_type="temperature",
            update_interval=update_interval,
            min_value=min_value,
            max_value=max_value,
            noise_level=noise_level,
            reading_class=TemperatureReading,
            reading_field="temperature",
        )
        self.pin = pin


class HumiditySensor(VirtualSensor):
    """Virtual humidity sensor for testing."""
    
    def __init__(
        self,
        name: str = "Virtual Humidity",
        update_interval: float = 1.0,
        min_value: float = 30.0,
        max_value: float = 70.0,
        noise_level: float = 0.5,
        pin: Optional[int] = None,
    ):
        """Initialize a virtual humidity sensor."""
        super().__init__(
            name=name,
            sensor_type="humidity",
            update_interval=update_interval,
            min_value=min_value,
            max_value=max_value,
            noise_level=noise_level,
            reading_class=HumidityReading,
            reading_field="humidity",
        )
        self.pin = pin

