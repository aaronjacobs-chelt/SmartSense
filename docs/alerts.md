# Alert System

The SmartSense alert system provides real-time notifications and automated responses when sensor readings meet specific conditions. This guide covers alert configuration, notification methods, and best practices.

## Alert System Overview

The SmartSense alert system consists of:

1. **Alert Conditions**: Rules that trigger alerts based on sensor data
2. **Alert Actions**: Responses that occur when conditions are met
3. **Alert Notifications**: Methods of informing users about alerts
4. **Alert History**: Record of past alert events for analysis

## Configuring Alerts

### Alert Creation

To create a new alert:

1. Navigate to **Settings > Alerts > Add Alert**
2. Select the sensor to monitor
3. Define the alert condition
4. Configure alert actions and notifications
5. Set severity level and optional schedule
6. Click **Save Alert**

### Alert Conditions

SmartSense supports various condition types:

#### Threshold Conditions

Trigger when a sensor reading crosses a defined threshold.

| Operator | Description | Example |
|----------|-------------|---------|
| gt | Greater than | Temperature > 25°C |
| lt | Less than | Humidity < 30% |
| gte | Greater than or equal to | Pressure >= 1020 hPa |
| lte | Less than or equal to | Battery <= 20%

