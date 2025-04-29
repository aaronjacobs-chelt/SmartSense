# Sensor Configuration

This guide provides detailed instructions for setting up and configuring sensors in the SmartSense system.

## Supported Sensor Types

SmartSense supports a wide range of sensor types for environmental monitoring:

| Sensor Type | Description | Available Models | Measurement Units |
|-------------|-------------|------------------|-------------------|
| Temperature | Measures ambient temperature | T100, T200, T300 | Celsius, Fahrenheit |
| Humidity | Measures relative humidity | H100, H200 | Percentage (%) |
| Pressure | Measures barometric pressure | P100, P200 | hPa, inHg |
| Light | Measures light intensity | L100, L200 | Lux |
| Motion | Detects movement | M100, M200 | Boolean (detected/not detected) |
| Door/Window | Detects open/closed state | DW100 | Boolean (open/closed) |
| Air Quality | Measures air quality (CO2, VOC) | AQ100, AQ200 | ppm, mg/m³ |
| Water Leak | Detects water presence | WL100 | Boolean (detected/not detected) |
| Soil Moisture | Measures soil water content | SM100 | Percentage (%) |

## Physical Sensor Setup

### General Setup Process

1. **Unbox and inspect** your sensor for any physical damage
2. **Power on** the sensor according to its specific instructions (battery, USB, or mains powered)
3. **Reset** the sensor if necessary (usually by holding a reset button for 5-10 seconds)
4. Follow the **sensor-specific connection** method below

### Connection Methods

SmartSense supports multiple connection methods:

#### Wi-Fi Sensors

1. Put the sensor in pairing mode (usually by holding a button for 3-5 seconds)
2. The sensor LED should blink rapidly, indicating it's in pairing mode
3. Use the SmartSense mobile app or web interface to add a new Wi-Fi sensor
4. Select your Wi-Fi network and enter credentials when prompted
5. The sensor should connect automatically and appear in your device list

#### Zigbee/Z-Wave Sensors

1. Ensure your SmartSense hub is properly set up and online
2. Put the hub in pairing mode through the app (Settings > Devices > Add Device)
3. Put the sensor in pairing mode according to its manual
4. The hub should detect the new sensor automatically
5. Name the sensor and assign it to a room/group when prompted

#### Bluetooth Sensors

1. Ensure Bluetooth is enabled on your SmartSense gateway device
2. Put the sensor in pairing mode
3. Use the SmartSense app to scan for new Bluetooth devices
4. Select your sensor from the list of discovered devices
5. Follow the prompts to complete pairing

#### Wired Sensors (GPIO)

1. Power off your SmartSense gateway device
2. Connect the sensor to the appropriate GPIO pins according to the pinout diagram
3. Power on the gateway
4. Use the web interface to configure the GPIO sensor (Settings > Devices > Add GPIO Sensor)

## Software Configuration

### Sensor Configuration Parameters

Each sensor type has specific configuration parameters that can be adjusted:

#### Common Parameters

| Parameter | Description | Default | Valid Range |
|-----------|-------------|---------|------------|
| name | User-friendly name | "New Sensor" | String |
| location | Physical location | "" | String |
| update_interval | Reading interval (seconds) | 60 | 1-86400 |
| enabled | Whether the sensor is active | True | Boolean |
| battery_low_threshold | Battery level alert threshold (%) | 20 | 5-50 |

#### Temperature Sensor Parameters

| Parameter | Description | Default | Valid Range |
|-----------|-------------|---------|------------|
| unit | Measurement unit | "celsius" | "celsius", "fahrenheit" |
| calibration_offset | Correction factor | 0.0 | -10.0 to 10.0 |
| threshold_high | High temperature alert threshold | 30.0 | -50.0 to 125.0 |
| threshold_low | Low temperature alert threshold | 5.0 | -50.0 to 125.0 |
| averaging_readings | Number of readings to average | 1 | 1-10 |

#### Humidity Sensor Parameters

| Parameter | Description | Default | Valid Range |
|-----------|-------------|---------|------------|
| calibration_offset | Correction factor | 0.0 | -10.0 to 10.0 |
| threshold_high | High humidity alert threshold | 75.0 | 0.0 to 100.0 |
| threshold_low | Low humidity alert threshold | 25.0 | 0.0 to 100.0 |
| averaging_readings | Number of readings to average | 1 | 1-10 |

#### Pressure Sensor Parameters

| Parameter | Description | Default | Valid Range |
|-----------|-------------|---------|------------|
| unit | Measurement unit | "hPa" | "hPa", "inHg" |
| calibration_offset | Correction factor | 0.0 | -100.0 to 100.0 |
| threshold_high | High pressure alert threshold | 1050.0 | 300.0 to 1100.0 |
| threshold_low | Low pressure alert threshold | 950.0 | 300.0 to 1100.0 |
| storm_change_threshold | Pressure change for storm alerts | 6.0 | 0.0 to 20.0 |

#### Air Quality Sensor Parameters

| Parameter | Description | Default | Valid Range |
|-----------|-------------|---------|------------|
| co2_threshold | CO2 alert threshold (ppm) | 1000.0 | 400.0 to 5000.0 |
| voc_threshold | VOC alert threshold (mg/m³) | 0.3 | 0.0 to 10.0 |
| calibration_period | Days between calibrations | 30 | 1-365 |

### Configuring via Web Interface

The easiest way to configure sensors is using the SmartSense web interface:

1. Navigate to **Settings > Devices**
2. Select the sensor you wish to configure
3. Update the parameters in the configuration form
4. Click **Save Changes** to apply

### Configuring via API

Sensors can also be configured programmatically using the SmartSense API:

```python
import requests

API_URL = "https://your-smartsense-instance/api/v1"
API_KEY = "your-api-key"

# Configure a temperature sensor
sensor_id = "sensor-uuid-here"

configuration = {
    "name": "Outdoor Temperature",
    "location": "backyard",
    "configuration": {
        "update_interval": 300,  # 5 minutes
        "unit": "celsius",
        "threshold_high": 35.0,
        "threshold_low": 5.0,
        "calibration_offset": -0.5  # Sensor reads 0.5°C high
    }
}

response = requests.put(
    f"{API_URL}/sensors/{sensor_id}",
    headers={"Authorization": f"ApiKey {API_KEY}"},
    json=configuration
)

print(response.json())
```

### Sensor Calibration

For maximum accuracy, sensors should be calibrated periodically:

1. Place a reference measurement device near the sensor
2. Note the readings from both devices
3. Calculate the difference
4. Apply this difference as a calibration_offset in the sensor configuration

### Troubleshooting Sensors

Common sensor issues and solutions:

**Sensor not connecting:**

- Ensure the sensor is within range of the network/hub
- Check battery level or power connection
- Reset the sensor and attempt the connection process again

**Erratic readings:**

- Increase the averaging_readings parameter
- Check for interference sources nearby
- Consider relocating the sensor

**Sensor frequently offline:**

- Check network signal strength at the sensor location
- Consider adding a network extender or mesh node
- For battery-powered sensors, check and replace batteries

**Consistently incorrect readings:**

- Apply a calibration_offset after comparing with a reference device
- Check for environmental factors (direct sunlight, heat sources, etc.)
- If persistent, the sensor may be defective and need replacement

## Virtual Sensors

SmartSense also supports virtual sensors that derive values from physical sensors or external data sources.

### Creating a Virtual Sensor

1. Navigate to **Settings > Devices > Add Virtual Sensor**
2. Select the virtual sensor type:
   - **Derived**: Calculate values from other sensors (e.g., dew point from temperature and humidity)
   - **Aggregate**: Combine readings from multiple sensors (e.g., average temperature)
   - **External**: Import data from external APIs (e.g., weather forecasts)
3. Configure the parameters according to the virtual sensor type
4. Click **Create Sensor**

### Virtual Sensor Examples

**Average Room Temperature:**

```json
{
  "name": "Average Home Temperature",
  "type": "virtual.aggregate",
  "aggregation_type": "average",
  "source_sensors": [
    "living-room-temp-sensor-id",
    "bedroom-temp-sensor-id",
    "kitchen-temp-sensor-id"
  ],
  "update_interval": 300
}
```

**Dew Point Calculation:**

```json
{
  "name": "Living Room Dew Point",
  "type": "virtual.derived",
  "derivation_type": "dewpoint",
  "source_sensors": {
    "temperature": "living-room-temp-sensor-id",
    "humidity": "living-room-humidity-sensor-id"
  },
  "update_interval": 300
}
```

## Next Steps

After configuring your sensors:

1. Set up [alerts](alerts.md) to be notified of important events
2. Configure your [dashboard](dashboard_setup.md) to visualize sensor data
3. Explore [automations](automations.md) to create responses to sensor conditions

For advanced configurations including custom sensor drivers, refer to the [Advanced Sensor Configuration](advanced_sensor_configuration.md) guide.
