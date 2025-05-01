"""
Core monitoring system for the SmartSense platform.

This module implements the central nervous system of the SmartSense platform,
including the SensorNetwork class that manages sensor connections, data collection,
storage, and event processing.
"""

import asyncio
import time
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union

from pydantic import BaseModel, Field

from smartsense.sensors.base import Sensor, SensorReading
from smartsense.utils.logging import get_logger

logger = get_logger(__name__)


class AlertAction(BaseModel):
    """Model for alert actions."""
    name: str
    callback: Callable
    description: Optional[str] = None


class AlertCondition(BaseModel):
    """Model for alert conditions."""
    sensor_id: str
    field: str
    operator: str  # 'gt', 'lt', 'eq', 'neq', 'between'
    value: Union[float, List[float]]
    comparison_buffer: float = 0.0  # To prevent alert flapping


class Alert(BaseModel):
    """Model for sensor alerts."""
    id: str
    name: str
    condition: AlertCondition
    actions: List[AlertAction]
    triggered: bool = False
    last_triggered: Optional[datetime] = None
    cooldown: int = 0  # Seconds between repeated alerts


class SensorNetwork:
    """
    Central class for managing a network of sensors.
    
    This class is responsible for:
    - Managing sensor registration and configuration
    - Collecting and storing sensor readings
    - Processing sensor data and triggering alerts
    - Providing access to real-time and historical data
    """
    
    def __init__(self, name: str = "SmartSense Network", update_interval: float = 1.0):
        """
        Initialize a new sensor network.
        
        Args:
            name: Human-readable name for this network
            update_interval: Default interval (in seconds) for sensor polling
        """
        self.name = name
        self.update_interval = update_interval
        self.sensors: Dict[str, Sensor] = {}
        self.readings: Dict[str, List[SensorReading]] = {}
        self.alerts: List[Alert] = []
        self.running: bool = False
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._tasks: Set[asyncio.Task] = set()
        
        logger.info(f"Initialized SensorNetwork '{name}' with update interval {update_interval}s")
    
    def add_sensor(self, sensor: Sensor) -> None:
        """
        Register a new sensor with the network.
        
        Args:
            sensor: Sensor instance to add to the network
        """
        if sensor.id in self.sensors:
            logger.warning(f"Sensor with ID '{sensor.id}' already exists, replacing")
        
        self.sensors[sensor.id] = sensor
        self.readings[sensor.id] = []
        logger.info(f"Added sensor: {sensor.name} (ID: {sensor.id}, Type: {sensor.type})")
    
    def remove_sensor(self, sensor_id: str) -> bool:
        """
        Remove a sensor from the network.
        
        Args:
            sensor_id: ID of the sensor to remove
            
        Returns:
            bool: True if removal was successful, False otherwise
        """
        if sensor_id in self.sensors:
            sensor = self.sensors.pop(sensor_id)
            self.readings.pop(sensor_id, None)
            logger.info(f"Removed sensor: {sensor.name} (ID: {sensor_id})")
            return True
        else:
            logger.warning(f"Attempted to remove non-existent sensor with ID: {sensor_id}")
            return False
    
    def add_alert(
        self, 
        sensor_id: str, 
        field: str,
        operator: str,
        value: Union[float, List[float]],
        actions: List[Tuple[str, Callable]],
        alert_name: Optional[str] = None,
        cooldown: int = 0
    ) -> str:
        """
        Create a new alert for a sensor.
        
        Args:
            sensor_id: ID of the sensor to monitor
            field: Field name to check (e.g., 'temperature')
            operator: Comparison operator ('gt', 'lt', 'eq', 'neq', 'between')
            value: Threshold value or range
            actions: List of (name, callback) tuples to execute when the alert triggers
            alert_name: Optional name for this alert
            cooldown: Seconds between repeated alerts
            
        Returns:
            str: ID of the created alert
        """
        if sensor_id not in self.sensors:
            raise ValueError(f"Sensor with ID '{sensor_id}' does not exist")
        
        # Generate alert ID and name if not provided
        alert_id = f"alert_{len(self.alerts) + 1}"
        if alert_name is None:
            alert_name = f"Alert for {self.sensors[sensor_id].name}.{field}"
        
        # Create alert actions
        alert_actions = []
        for name, callback in actions:
            alert_actions.append(AlertAction(name=name, callback=callback))
        
        # Create alert condition
        condition = AlertCondition(
            sensor_id=sensor_id,
            field=field,
            operator=operator,
            value=value
        )
        
        # Create and register the alert
        alert = Alert(
            id=alert_id,
            name=alert_name,
            condition=condition,
            actions=alert_actions,
            cooldown=cooldown
        )
        
        self.alerts.append(alert)
        logger.info(f"Created alert '{alert_name}' for {self.sensors[sensor_id].name}.{field}")
        
        return alert_id
    
    async def _poll_sensor(self, sensor: Sensor) -> None:
        """
        Poll a sensor for data at its defined interval.
        
        Args:
            sensor: Sensor to poll
        """
        while self.running:
            try:
                reading = await sensor.read()
                if reading:
                    self.readings[sensor.id].append(reading)
                    # Process alerts for this sensor
                    await self._process_alerts(sensor.id, reading)
                    
                    # Log at appropriate level
                    if len(self.readings[sensor.id]) % 100 == 0:  # Log every 100 readings
                        logger.info(f"Collected {len(self.readings[sensor.id])} readings from {sensor.name}")
                    else:
                        logger.debug(f"New reading from {sensor.name}: {reading}")
            
            except Exception as e:
                logger.error(f"Error polling sensor {sensor.name}: {str(e)}")
            
            # Sleep for the sensor's update interval
            await asyncio.sleep(sensor.update_interval)
    
    async def _process_alerts(self, sensor_id: str, reading: SensorReading) -> None:
        """
        Process all alerts for a given sensor reading.
        
        Args:
            sensor_id: ID of the sensor
            reading: New sensor reading to check against alert conditions
        """
        for alert in self.alerts:
            if alert.condition.sensor_id != sensor_id:
                continue
                
            # Check if the alert field exists in the reading
            field = alert.condition.field
            if not hasattr(reading, field):
                logger.warning(f"Field '{field}' not found in reading from sensor {sensor_id}")
                continue
            
            # Get the value to check
            value = getattr(reading, field)
            
            # Check the alert condition
            triggered = False
            operator = alert.condition.operator
            threshold = alert.condition.value
            
            if operator == "gt":
                triggered = value > threshold
            elif operator == "lt":
                triggered = value < threshold
            elif operator == "eq":
                triggered = abs(value - threshold) <= alert.condition.comparison_buffer
            elif operator == "neq":
                triggered = abs(value - threshold) > alert.condition.comparison_buffer
            elif operator == "between" and isinstance(threshold, list) and len(threshold) == 2:
                triggered = threshold[0] <= value <= threshold[1]
            
            # Handle alert state changes
            now = datetime.now()
            cooldown_ok = True
            
            if alert.last_triggered:
                elapsed = (now - alert.last_triggered).total_seconds()
                cooldown_ok = elapsed > alert.cooldown
            
            if triggered and not alert.triggered and cooldown_ok:
                # Alert just triggered
                alert.triggered = True
                alert.last_triggered = now
                
                # Execute actions
                for action in alert.actions:
                    try:
                        action.callback()
                        logger.info(f"Executed action '{action.name}' for alert '{alert.name}'")
                    except Exception as e:
                        logger.error(f"Error executing action '{action.name}': {str(e)}")
                
                logger.warning(f"Alert '{alert.name}' triggered: {field}={value}")
                
            elif not triggered and alert.triggered:
                # Alert condition no longer met
                alert.triggered = False
                logger.info(f"Alert '{alert.name}' cleared: {field}={value}")
    
    async def _run_network(self) -> None:
        """Internal method to run the sensor network.
        
        This method creates and manages polling tasks for all registered sensors.
        It runs continuously while self.running is True, creating tasks for new sensors
        and cleaning up completed or cancelled tasks.
        """
        try:
            # Create initial polling tasks for all registered sensors
            for sensor_id, sensor in self.sensors.items():
                if self.running:  # Check if still running before creating each task
                    task = asyncio.create_task(self._poll_sensor(sensor))
                    self._tasks.add(task)
                    # Set callback to remove task from set when done
                    task.add_done_callback(self._tasks.discard)
                    logger.debug(f"Started polling task for sensor: {sensor.name}")
            
            # Continue running until explicitly stopped
            while self.running:
                # Check for any tasks that have failed
                for task in list(self._tasks):
                    if task.done() and not task.cancelled():
                        try:
                            # This will re-raise any exception that occurred in the task
                            task.result()
                        except Exception as e:
                            logger.error(f"Sensor polling task failed: {str(e)}")
                
                # Sleep briefly to avoid high CPU usage
                await asyncio.sleep(0.1)
                
        except asyncio.CancelledError:
            logger.info("Network run task was cancelled")
            raise
        except Exception as e:
            logger.error(f"Error in network run loop: {str(e)}")
        finally:
            # Cleanup: cancel all polling tasks when the network stops
            for task in self._tasks:
                if not task.done():
                    task.cancel()
            
            # Wait for all tasks to complete their cancellation
            if self._tasks:
                await asyncio.gather(*self._tasks, return_exceptions=True)
                self._tasks.clear()
                
            logger.info("Sensor network stopped")

