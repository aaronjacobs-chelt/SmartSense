### Temperature & Humidity Sensors

| Sensor | Interface | Accuracy | Power | Price Range | Notes |
|--------|-----------|----------|-------|-------------|-------|
| DHT22 | Digital (1-Wire) | ±0.5°C, ±2-5% RH | 3.3-5V, ~1.5mA | $5-10 | Good balance of accuracy and cost |
| DHT11 | Digital (1-Wire) | ±2°C, ±5% RH | 3.3-5V, ~0.3mA | $2-5 | Lower accuracy, good for beginners |
| BME280 | I2C/SPI | ±0.5°C, ±3% RH | 3.3V, ~3.6µA | $8-15 | Includes pressure sensor, very accurate |
| SHT31 | I2C | ±0.3°C, ±2% RH | 3.3V, ~1.5mA | $10-20 | High accuracy, industrial grade |
| AM2320 | I2C | ±0.5°C, ±3% RH | 3.3-5V, ~1mA | $5-8 | Improved DHT22 with I2C interface |
| HTU21D | I2C | ±0.3°C, ±2% RH | 3.3V, ~0.5mA | $8-15 | Good accuracy, low power |

### Pressure Sensors

| Sensor | Interface | Accuracy | Range | Power | Price Range | Notes |
|--------|-----------|----------|-------|-------|-------------|-------|
| BMP280 | I2C/SPI | ±1 hPa | 300-1100 hPa | 3.3V, ~2.7µA | $5-10 | Temperature included, no humidity |
| BME280 | I2C/SPI | ±1 hPa | 300-1100 hPa | 3.3V, ~3.6µA | $8-15 | Temperature and humidity included |
| BMP388 | I2C/SPI | ±0.5 hPa | 300-1250 hPa | 3.3V, ~3.4µA | $10-18 | High precision, altitude measurement |
| MS5611 | I2C/SPI | ±1.5 hPa | 10-1200 hPa | 3.3V, ~1µA | $15-25 | High altitude resolution (10cm) |
| LPS22HB | I2C/SPI | ±1 hPa | 260-1260 hPa | 3.3V, ~4µA | $5-12 | Ultra-low power |

### Light Sensors

| Sensor | Interface | Spectral Range | Resolution | Power | Price Range | Notes |
|--------|-----------|----------------|------------|-------|-------------|-------|
| BH1750 | I2C | Visible | 1-65535 lux | 3.3-5V, ~0.2mA | $3-8 | Matches human eye response |
| TSL2561 | I2C | Visible + IR | 0.1-40000 lux | 3.3V, ~0.6mA | $5-12 | IR and visible light channels |
| VEML6070 | I2C | UV | UV index | 3.3-5V, ~0.1mA | $5-10 | UV radiation specific |
| VEML7700 | I2C | Visible | 0-120000 lux | 3.3V, ~0.5mA | $4-10 | High dynamic range |
| LTR-329ALS | I2C | Visible | 0.01-64k lux | 3.3V, ~0.1mA | $3-8 | Low power consumption |

### Air Quality Sensors

| Sensor | Interface | Measures | Accuracy | Power | Price Range | Notes |
|--------|-----------|----------|----------|-------|-------------|-------|
| MQ-135 | Analog | CO2, NH3, NOx | Qualitative | 5V, ~150mA | $3-8 | Requires calibration, high power |
| CCS811 | I2C | CO2, VOCs | ±15% | 3.3V, ~30mA | $15-25 | Good for indoor air quality |
| SGP30 | I2C | VOCs, H2 | Qualitative | 3.3V, ~50mA | $15-25 | Self-calibrating, accurate |
| SCD30 | I2C | CO2, Temp, RH | ±30ppm | 3.3-5V, ~50mA | $40-60 | NDIR CO2 sensor, very accurate |
| BME680 | I2C/SPI | VOCs, Temp, Pressure, RH | Qualitative | 3.3V, ~3.7µA | $15-25 | All-in-one environmental sensor |

### Motion & Distance Sensors

| Sensor | Interface | Range | Accuracy | Power | Price Range | Notes |
|--------|-----------|-------|----------|-------|-------------|-------|
| PIR HC-SR501 | Digital | ~7m | N/A | 5V, ~50µA | $2-5 | Motion detection only |
| HC-SR04 | Digital | 2-400cm | ±3mm | 5V, ~15mA | $2-5 | Ultrasonic distance sensor |
| VL53L0X | I2C | 5-120cm | ±3% | 3.3V, ~20mA | $5-15 | Time-of-flight laser distance |
| RCWL-0516 | Digital | ~7m | N/A | 5V, ~3mA | $3-7 | Microwave motion detection |
| GP2Y0A21YK | Analog | 10-80cm | ±10% | 5V, ~30mA | $8-15 | IR distance sensor |

### Water & Soil Sensors

| Sensor | Interface | Measures | Accuracy | Power | Price Range | Notes |
|--------|-----------|----------|----------|-------|-------------|-------|
| Capacitive Soil Moisture | Analog | Moisture % | Qualitative | 3.3-5V, ~5mA | $3-10 | Doesn't corrode like resistive |
| DS18B20 Waterproof | Digital (1-Wire) | Temperature | ±0.5°C | 3.3-5V, ~1mA | $3-8 | Waterproof temperature probe |
| pH Sensor | Analog | pH 0-14 | ±0.1 pH | 5V, ~5-10mA | $30-60 | Requires calibration |
| EC Sensor | Analog | Conductivity | ±5% | 5V, ~5-10mA | $30-60 | Measures nutrient levels |
| Water Flow YF-S201 | Digital (Pulse) | Flow rate | ±10% | 5V, ~15mA | $8-15 | Hall effect flow meter |
| Water Level | Analog | Level | Qualitative | 5V, ~20mA | $3-10 | Float or capacitive options |

## Connection & Wiring Diagrams

This section provides standard wiring diagrams for connecting various sensors to supported platforms.

### Raspberry Pi GPIO Pinout

![Raspberry Pi GPIO Pinout](images/rpi_pinout.png)

*Note: Create this diagram or source one with appropriate licensing.*

### Common Sensor Connections

#### I2C Sensors (e.g., BME280, BH1750)

```
Raspberry Pi    Sensor
-------------   ------
3.3V        ->  VCC
GND         ->  GND
GPIO2 (SDA) ->  SDA
GPIO3 (SCL) ->  SCL
```

![I2C Sensor Connection](images/i2c_connection.png)

*Note: Create this diagram showing the connections.*

#### One-Wire Sensors (e.g., DHT22, DS18B20)

```
Raspberry Pi    Sensor         Notes
-------------   ------         -----
3.3V or 5V  ->  VCC            Check sensor voltage requirements
GND         ->  GND
GPIO4       ->  DATA           Include a 4.7kΩ pull-up resistor between DATA and VCC
```

![One-Wire Sensor Connection](images/onewire_connection.png)

*Note: Create this diagram showing the connections including the pull-up resistor.*

#### Analog Sensors with MCP3008 ADC

Since the Raspberry Pi doesn't have analog inputs, an ADC (Analog-to-Digital Converter) like the MCP3008 is required for analog sensors:

```
Raspberry Pi    MCP3008         Notes
-------------   -------         -----
3.3V        ->  VDD, VREF       
GND         ->  DGND, AGND
GPIO10      ->  MOSI
GPIO9       ->  MISO
GPIO11      ->  CLK
GPIO8       ->  CS/SHDN

MCP3008         Analog Sensor
-------         -------------
CH0-7       ->  SIGNAL         Connect to appropriate channel
```

![Analog Sensor with ADC Connection](images/adc_connection.png)

*Note: Create this diagram showing the connections.*

### Multi-Sensor Setup

For a typical environmental monitoring station with multiple sensors:

![Multi-Sensor Setup](images/multi_sensor_setup.png)

*Note: Create a comprehensive diagram showing multiple sensors connected to a Raspberry Pi.*

## Power Requirements

### Power Calculation

To calculate the power requirements for your SmartSense installation, add up the current draw of all connected components:

| Component | Typical Current Draw |
|-----------|----------------------|
| Raspberry Pi 4B | ~600-1000mA |
| Raspberry Pi 3B+ | ~500-700mA |
| Raspberry Pi Zero 2W | ~150-300mA |
| DHT22 Sensor | ~1.5mA |
| BME280 Sensor | ~3.6µA |
| BH1750 Light Sensor | ~0.2mA |
| PIR Motion Sensor | ~50µA (idle), ~5mA (active) |
| MCP3008 ADC | ~0.5mA |

**Example Calculation:**
- Raspberry Pi 4B: 700mA
- 3× BME280 sensors: 3 × 0.0036mA ≈ 0.01mA
- 2× PIR sensors: 2 × 5mA = 10mA
- BH1750 light sensor: 0.2mA
- Total: 710.21mA

For reliable operation, choose a power supply rated for at least 25% more than your calculated requirement.

### Battery Operation

For battery-powered installations:

| Battery Type | Capacity | Approximate Runtime | Notes |
|--------------|----------|---------------------|-------|
| 18650 Li-ion (2S1P) | 6000-7000mAh | 8-10 hours | For Raspberry Pi with 4-5 sensors |
| 6x AA Alkaline | 2000-2500mAh | 2-3 hours | Budget option |
| 12V Lead Acid | 7-12Ah | 24-48 hours | Larger installations |
| Solar + 18650 (2S2P) | 12000-14000mAh + 5W panel | Continuous | Good for outdoor installations |

**Power Saving Tips:**
- Reduce polling frequency for sensors
- Use lower power SBCs like Raspberry Pi Zero 2W for small installations
- Implement sleep modes between readings
- Disable unused hardware (HDMI, WiFi, etc.)
- Consider using ESP32 as remote sensor nodes with low-power modes

## Installation & Assembly

### Recommended Enclosures

| Enclosure Type | Dimensions | IP Rating | Use Case | Price Range |
|----------------|------------|-----------|----------|-------------|
| ABS Plastic Box | 100x60x25mm | IP54 | Indoor sensors | $5-15 |
| Weatherproof Box | 150x100x70mm | IP65+ | Outdoor deployments | $15-30 |
| DIN Rail Enclosure | Standard DIN | IP20 | Industrial installations | $20-40 |
| 3D Printed Custom | Various | Varies | Custom sensor arrays | Material cost |
| Metal Case | Various | IP40-IP65 | EMI sensitive environments | $25-50 |

### Recommended Accessories

| Accessory | Purpose | Recommendation |
|-----------|---------|----------------|
| Power Supply | Main power | 5V 3A USB-C adapter for Raspberry Pi 4 |
| MicroSD Card | OS & storage | SanDisk Extreme Pro 32GB+ A2 rated |
| Heat Sinks | Cooling | Aluminum heat sink kit for SBC |
| Cooling Fan | Active cooling | 5V 30mm fan for high-performance setups |
| Standoffs | Circuit mounting | M2.5 nylon standoffs with screws |
| Jumper Wires | Connections | Dupont jumper wire kit, male-to-female and female-to-female |
| Terminal Blocks | Secure connections | Screw terminal blocks for permanent installations |
| Breadboard | Prototyping | Half-size or full-size solderless breadboard |
| RTC Module | Time keeping | DS3231 I2C RTC for offline time tracking |

## Assembly Instructions

### Basic Indoor Environmental Station

1. **Prepare the Raspberry Pi**
   - Install operating system using Raspberry Pi Imager
   - Enable SSH, I2C, and One-Wire interfaces in `raspi-config`
   - Update system: `sudo apt update && sudo apt upgrade`

2. **Install Required Libraries**
   ```bash
   sudo apt install python3-pip python3-smbus i2c-tools
   sudo pip3 install RPi.GPIO adafruit-blinka adafruit-circuitpython-bme280
   ```

3. **Connect the Sensors**
   - Connect BME280 to I2C pins (GPIO2, GPIO3) with appropriate power
   - Connect BH1750 to same I2C bus with unique address
   - Connect any one-wire sensors to GPIO4 with pull-up resistors

4. **Install SmartSense**
   ```bash
   sudo pip3 install smartsense
   ```

5. **Create Configuration File**
   - Create `config.yml` using template from documentation
   - Specify sensors and their parameters

6. **Start SmartSense**
   ```bash
   smartsense --config config.yml
   ```

7. **Access Dashboard**
   - Open web browser to `http://<raspberry-pi-ip>:8050`

### Weatherproof Outdoor Station

For outdoor installations, additional steps are required:

1. **Prepare the Weatherproof Enclosure**
   - Drill holes for sensor probes and cable glands
   - Seal all openings with appropriate weatherproof seals

2. **Use Appropriate Cabling**
   - Use UV-resistant, waterproof cables for external connections
   - Consider shielded cables in areas with EMI

3. **Add Desiccant
