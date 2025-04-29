"""
FastAPI routes for the SmartSense API.

This module defines the RESTful API endpoints for the SmartSense platform.
It provides endpoints for sensor management, data access, and system control.
"""

import asyncio
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from smartsense.core.monitor import SensorNetwork
from smartsense.sensors.base import Sensor, SensorReading
from smartsense.utils.logging import get_logger

logger = get_logger(__name__)

# Models for API requests and responses
class SensorMetadata(BaseModel):
    """Model for sensor metadata."""
    
    id: str
    name: str
    type: str
    update_interval: float
    last_read_time: Optional[float] = None
    pin: Optional[int] = None


class SensorReadingResponse(BaseModel):
    """Model for sensor reading response."""
    
    sensor_id: str
    timestamp: datetime
    values: Dict[str, Any]


class SensorDataResponse(BaseModel):
    """Model for sensor data response with multiple readings."""
    
    sensor: SensorMetadata
    readings: List[SensorReadingResponse]


class AlertResponse(BaseModel):
    """Model for alert response."""
    
    id: str
    name: str
    sensor_id: str
    field: str
    operator: str
    value: Union[float, List[float]]
    triggered: bool
    last_triggered: Optional[datetime] = None


class CreateAlertRequest(BaseModel):
    """Model for creating a new alert."""
    
    sensor_id: str
    field: str
    operator: str
    value: Union[float, List[float]]
    name: Optional[str] = None
    cooldown: int = 0


class NetworkStatusResponse(BaseModel):
    """Model for network status response."""
    
    name: str
    running: bool
    sensor_count: int
    alert_count: int
    update_interval: float


# API Router setup
router = APIRouter(prefix="/api/v1")


# Dependency to get the sensor network
async def get_network() -> SensorNetwork:
    """Get the global sensor network."""
    # This would normally use a dependency injection system
    # For now, we'll simulate having a global network instance
    from smartsense import network
    return network


@router.get("/", response_model=Dict[str, str])
async def root() -> Dict[str, str]:
    """Root endpoint returning API info."""
    return {
        "name": "SmartSense API",
        "version": "1.0.0",
        "documentation": "/docs",
    }


@router.get("/status", response_model=NetworkStatusResponse)
async def get_status(network: SensorNetwork = Depends(get_network)) -> NetworkStatusResponse:
    """Get the current status of the sensor network."""
    return NetworkStatusResponse(
        name=network.name,
        running=network.running,
        sensor_count=len(network.sensors),
        alert_count=len(network.alerts),
        update_interval=network.update_interval,
    )


@router.get("/sensors", response_model=List[SensorMetadata])
async def list_sensors(network: SensorNetwork = Depends(get_network)) -> List[SensorMetadata]:
    """List all sensors in the network."""
    return [SensorMetadata(**sensor.get_metadata()) for sensor in network.sensors.values()]

@router.get("/sensors/{sensor_id}", response_model=SensorMetadata)
async def get_sensor(sensor_id: str, network: SensorNetwork = Depends(get_network)) -> SensorMetadata:
    """
    Get metadata for a specific sensor.
    
    Args:
        sensor_id: ID of the sensor to retrieve
        network: Sensor network instance
    
    Returns:
        SensorMetadata: Metadata for the requested sensor
    
    Raises:
        HTTPException: If the sensor is not found
    """
    if sensor_id not in network.sensors:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor with ID '{sensor_id}' not found",
        )
    
    sensor = network.sensors[sensor_id]
    return SensorMetadata(**sensor.get_metadata())


@router.get("/sensors/{sensor_id}/readings", response_model=SensorDataResponse)
async def get_sensor_readings(
    sensor_id: str,
    limit: int = Query(10, ge=1, le=1000),
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    network: SensorNetwork = Depends(get_network),
) -> SensorDataResponse:
    """
    Get readings for a specific sensor.
    
    Args:
        sensor_id: ID of the sensor to retrieve readings for
        limit: Maximum number of readings to return
        start_time: Filter readings from this time onwards
        end_time: Filter readings up to this time
        network: Sensor network instance
    
    Returns:
        SensorDataResponse: Sensor metadata and readings
    
    Raises:
        HTTPException: If the sensor is not found
    """
    if sensor_id not in network.sensors:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor with ID '{sensor_id}' not found",
        )
    
    sensor = network.sensors[sensor_id]
    readings = network.readings.get(sensor_id, [])
    
    # Apply time filters if provided
    if start_time:
        readings = [r for r in readings if r.timestamp >= start_time]
    if end_time:
        readings = [r for r in readings if r.timestamp <= end_time]
    
    # Apply limit and convert to response format
    readings = readings[-limit:]
    
    reading_responses = []
    for reading in readings:
        reading_dict = reading.dict()
        values = {k: v for k, v in reading_dict.items() if k not in ["timestamp", "sensor_id"]}
        reading_responses.append(
            SensorReadingResponse(
                sensor_id=reading.sensor_id,
                timestamp=reading.timestamp,
                values=values,
            )
        )
    
    return SensorDataResponse(
        sensor=SensorMetadata(**sensor.get_metadata()),
        readings=reading_responses,
    )


@router.get("/sensors/{sensor_id}/current", response_model=SensorReadingResponse)
async def get_current_reading(
    sensor_id: str,
    network: SensorNetwork = Depends(get_network),
) -> SensorReadingResponse:
    """
    Get the most recent reading for a specific sensor.
    
    Args:
        sensor_id: ID of the sensor to retrieve the reading for
        network: Sensor network instance
    
    Returns:
        SensorReadingResponse: The most recent sensor reading
    
    Raises:
        HTTPException: If the sensor is not found or has no readings
    """
    if sensor_id not in network.sensors:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor with ID '{sensor_id}' not found",
        )
    
    sensor = network.sensors[sensor_id]
    reading = sensor.get_last_reading()
    
    if not reading:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No readings available for sensor '{sensor_id}'",
        )
    
    reading_dict = reading.dict()
    values = {k: v for k, v in reading_dict.items() if k not in ["timestamp", "sensor_id"]}
    
    return SensorReadingResponse(
        sensor_id=reading.sensor_id,
        timestamp=reading.timestamp,
        values=values,
    )


@router.get("/alerts", response_model=List[AlertResponse])
async def list_alerts(network: SensorNetwork = Depends(get_network)) -> List[AlertResponse]:
    """
    List all alerts in the network.
    
    Args:
        network: Sensor network instance
    
    Returns:
        List[AlertResponse]: List of alert metadata
    """
    return [
        AlertResponse(
            id=alert.id,
            name=alert.name,
            sensor_id=alert.condition.sensor_id,
            field=alert.condition.field,
            operator=alert.condition.operator,
            value=alert.condition.value,
            triggered=alert.triggered,
            last_triggered=alert.last_triggered,
        )
        for alert in network.alerts
    ]


@router.post("/alerts", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
async def create_alert(
    alert_request: CreateAlertRequest,
    network: SensorNetwork = Depends(get_network),
) -> AlertResponse:
    """
    Create a new alert.
    
    Args:
        alert_request: Alert configuration
        network: Sensor network instance
    
    Returns:
        AlertResponse: The created alert
    
    Raises:
        HTTPException: If the sensor is not found or the alert configuration is invalid
    """
    if alert_request.sensor_id not in network.sensors:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor with ID '{alert_request.sensor_id}' not found",
        )
    
    # Validate the operator
    valid_operators = ["gt", "lt", "eq", "neq", "between"]
    if alert_request.operator not in valid_operators:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid operator: {alert_request.operator}. Must be one of {valid_operators}",
        )
    
    # For now, we'll use a placeholder action that logs the alert
    def log_alert_action():
        logger.warning(f"Alert triggered for {alert_request.sensor_id}.{alert_request.field}")
    
    try:
        alert_id = network.add_alert(
            sensor_id=alert_request.sensor_id,
            field=alert_request.field,
            operator=alert_request.operator,
            value=alert_request.value,
            actions=[("log", log_alert_action)],
            alert_name=alert_request.name,
            cooldown=alert_request.cooldown,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
    # Find the created alert
    for alert in network.alerts:
        if alert.id == alert_id:
            return AlertResponse(
                id=alert.id,
                name=alert.name,
                sensor_id=alert.condition.sensor_id,
                field=alert.condition.field,
                operator=alert.condition.operator,
                value=alert.condition.value,
                triggered=alert.triggered,
                last_triggered=alert.last_triggered,
            )
    
    # This should never happen
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Alert was created but could not be retrieved",
    )


@router.delete("/alerts/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_alert(
    alert_id: str,
    network: SensorNetwork = Depends(get_network),
) -> None:
    """
    Delete an alert.
    
    Args:
        alert_id: ID of the alert to delete
        network: Sensor network instance
    
    Raises:
        HTTPException: If the alert is not found
    """
    # Find and remove the alert
    for i, alert in enumerate(network.alerts):
        if alert.id == alert_id:
            network.alerts.pop(i)
            return
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Alert with ID '{alert_id}' not found",
    )


@router.post("/network/start", response_model=NetworkStatusResponse)
async def start_network(network: SensorNetwork = Depends(get_network)) -> NetworkStatusResponse:
    """
    Start the sensor network.
    
    Args:
        network: Sensor network instance
    
    Returns:
        NetworkStatusResponse: Updated network status
    """
    if not network.running:
        # In a real implementation, this would start the network
        # For now, we'll just set the flag
        network.running = True
        logger.info(f"Started sensor network: {network.name}")
    
    return NetworkStatusResponse(
        name=network.name,
        running=network.running,
        sensor_count=len(network.sensors),
        alert_count=len(network.alerts),
        update_interval=network.update_interval,
    )


@router.post("/network/stop", response_model=NetworkStatusResponse)
async def stop_network(network: SensorNetwork = Depends(get_network)) -> NetworkStatusResponse:
    """
    Stop the sensor network.
    
    Args:
        network: Sensor network instance
    
    Returns:
        NetworkStatusResponse: Updated network status
    """
    if network.running:
        # In a real implementation, this would stop the network
        # For now, we'll just set the flag
        network.running = False
        logger.info(f"Stopped sensor network: {network.name}")
    
    return NetworkStatusResponse(
        name=network.name,
        running=network.running,
        sensor_count=len(network.sensors),
        alert_count=len(network.alerts),
        update_interval=network.update_interval,
    )


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured FastAPI application
    """
    app = FastAPI(
        title="SmartSense API",
        description="API for the SmartSense IoT platform",
        version="1.0.0",
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include the router
    app.include_router(router)
    
    return app

