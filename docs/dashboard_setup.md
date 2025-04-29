# Dashboard Setup

This guide provides instructions for setting up and customizing the SmartSense dashboard to monitor your environmental data effectively.

## Dashboard Overview

The SmartSense dashboard is a powerful visualization tool that displays your sensor data in real-time. It features:

- Customizable widgets for different data types
- User-configurable layouts and themes
- Interactive charts and graphs
- Alert notifications and status indicators
- Multiple dashboard support for different use cases

![Dashboard Preview](images/dashboard_preview.png)

## Getting Started

### Accessing the Dashboard

The SmartSense dashboard can be accessed through multiple interfaces:

- **Web Interface**: Navigate to `https://your-smartsense-instance/dashboard` in your web browser
- **Mobile App**: Open the SmartSense app on your iOS or Android device
- **Local Display**: If you have a dedicated display device set up (e.g., Raspberry Pi with touchscreen)

### Default Dashboard

Upon initial setup, SmartSense creates a default dashboard with basic widgets for your configured sensors. This provides a starting point for your customization.

## Dashboard Customization

### Creating a New Dashboard

1. In the web interface, click the **+** button next to the dashboard tabs
2. Enter a name for your new dashboard (e.g., "Home Environment", "Garden Sensors")
3. Select a layout template:
   - **Grid**: Traditional widget grid layout
   - **Freeform**: Drag and position widgets anywhere
   - **Vertical Panels**: Scrollable vertical panels
4. Click **Create Dashboard**

### Adding Widgets

1. In edit mode, click the **Add Widget** button
2. Select the widget type:
   - **Gauge**: For single values with thresholds
   - **Chart**: For time-series data
   - **Status**: For binary sensors (on/off, open/closed)
   - **Value**: For simple numeric display
   - **Alert**: For displaying sensor alerts
   - **Map**: For geospatial data visualization
   - **Camera**: For video feeds (if configured)
   - **Custom**: For advanced HTML/JavaScript widgets
3. Configure the widget:
   - Select the data source (sensor)
   - Choose visualization options
   - Set refresh rate and time window
   - Configure thresholds and alert colors
4. Click **Add to Dashboard**

### Widget Configuration Options

#### Chart Widget

| Option | Description | Default |
|--------|-------------|---------|
| Title | Widget display name | Sensor name |
| Chart Type | Line, Bar, Area, or Scatter | Line |
| Time Range | Historical data to display | 24 hours |
| Auto Refresh | Update frequency | 60 seconds |
| Y-Axis Range | Manual or automatic scaling | Auto |
| Stacking | Stack multiple series | Off |
| Threshold Lines | Show alert thresholds | On |

#### Gauge Widget

| Option | Description | Default |
|--------|-------------|---------|
| Title | Widget display name | Sensor name |
| Min/Max Values | Value range | Sensor-specific |
| Thresholds | Color ranges on gauge | Sensor alert thresholds |
| Unit | Measurement unit to display | Sensor-specific |
| Decimal Places | Precision of displayed value | 1 |

### Layout Customization

In edit mode, you can:

- **Resize** widgets by dragging their corners
- **Reposition** widgets by dragging them to new locations
- **Remove** widgets by clicking the X in their top right corner
- **Clone** widgets by clicking the duplicate icon

### Theme Customization

1. Navigate to **Dashboard Settings > Appearance**
2. Choose a predefined theme (Light, Dark, High Contrast)
3. Or customize your own:
   - Background color/image
   - Widget background and border colors
   - Font styles and sizes
   - Chart colors and styles

### Saving and Sharing Dashboards

1. Click **Save Layout** to preserve your changes
2. To share a dashboard:
   - Click **Dashboard Settings > Sharing**
   - Enable **Public Access** (optional, for external sharing)
   - Set a share password (recommended)
   - Copy the share URL to distribute

## Advanced Dashboard Features

### Creating Dashboard Templates

For consistent dashboards across multiple locations or deployments:

1. Configure a dashboard as desired
2. Go to **Dashboard Settings > Save as Template**
3. Name your template and add a description
4. The template will appear in the template list when creating new dashboards

### Automated Dashboard Rotation

For display on dedicated screens (like a wall-mounted tablet):

1. Go to **Dashboard Settings > Display Options**
2. Enable **Dashboard Rotation**
3. Select dashboards to include in rotation
4. Set the rotation interval (in seconds)
5. Optionally enable **Kiosk Mode** to hide navigation elements

### Dashboard Export/Import

To back up or transfer dashboard configurations:

1. Go to **Dashboard Settings > Advanced**
2. Click **Export Dashboard Configuration**
3. Save the JSON file
4. To import, go to **Dashboard Settings > Advanced** on another instance
5. Click **Import Dashboard Configuration** and select your saved file

### Creating Custom Widgets

Advanced users can create custom widgets:

1. Go to **Add Widget > Custom**
2. Select the data source(s)
3. Edit the HTML/CSS/JavaScript in the code editor
4. Use the `data` object to access sensor values
5. Click **Preview** to test your widget
6. Click **Save** when complete

Example custom widget code:

```html
<div class="custom-widget">
  <div class="temperature" 
       style="font-size: {{data.value > 25 ? '150%' : '120%'}}; 
              color: {{data.value > 30 ? '#ff0000' : 
                      (data.value < 15 ? '#0000ff' : '#000000')}}">
    {{data.value}}°C
  </div>
  <div class="trend">
    {{data.trend > 0 ? '↑' : (data.trend < 0 ? '↓' : '→')}}
  </div>
</div>
```

## Mobile Dashboard

The SmartSense mobile app provides dashboard access with additional features:

- Optimized layouts for smaller screens
- Push notifications for alerts
- Widget-specific gestures
- Offline caching of recent data

To customize the mobile dashboard:

1. Open the SmartSense mobile app
2. Go to **Settings > Dashboard > Customize**
3. Arrange widgets with touch gestures
4. Configure mobile-specific options (e.g., notification preferences)

## Troubleshooting

Common dashboard issues and solutions:

### Dashboard Not Loading

- Clear your browser cache
- Check your network connection
- Verify your SmartSense instance is running
- Check for browser console errors

### Widgets Not Updating

- Check the auto-refresh setting for the widget
- Verify the sensor is online and reporting data
- Check your network connection
- Try manually refreshing the dashboard

### Performance Issues

- Reduce the number of widgets per dashboard
- Increase widget refresh intervals
- Disable animations in Dashboard Settings
- For resource-constrained devices, use the "Lite" dashboard mode

## Next Steps

After setting up your dashboard:

- Configure [alerts](alerts.md) to be notified of important events
- Set up [automated actions](automations.md) based on sensor readings
- Explore [integrations](integrations.md) with other systems and services

