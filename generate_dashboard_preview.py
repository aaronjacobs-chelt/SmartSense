#!/usr/bin/env python3
"""
Script to generate a placeholder dashboard image for SmartSense.
This creates a simple visualization with key dashboard elements.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from datetime import datetime, timedelta

# Create the figure and grid layout
plt.figure(figsize=(10, 6), dpi=100)  # 1000x600 pixels
plt.style.use('dark_background')

# Set up the grid layout
gs = GridSpec(3, 4, figure=plt.gcf())

# Title and header
plt.figtext(0.5, 0.97, 'SmartSense Dashboard', fontsize=18, ha='center', color='white')
plt.figtext(0.5, 0.93, 'Home Environment Monitoring System', fontsize=12, ha='center', color='#8a8a8a')

# Create a fake time series data
timestamps = [datetime.now() - timedelta(hours=i) for i in range(24, 0, -1)]
temperatures = [22 + np.sin(i/3) + np.random.normal(0, 0.3) for i in range(24)]
humidity = [45 + np.cos(i/4) * 5 + np.random.normal(0, 1) for i in range(24)]

# Temperature chart
ax1 = plt.subplot(gs[0:2, 0:2])
ax1.plot([t.strftime('%H:%M') for t in timestamps[::2]], temperatures[::2], 'r-', linewidth=2)
ax1.set_title('Temperature (°C)', color='white')
ax1.set_facecolor('#1e1e1e')
ax1.grid(color='#333333', linestyle='-', linewidth=0.5)
ax1.tick_params(colors='#8a8a8a')
ax1.set_xlim(timestamps[-1].strftime('%H:%M'), timestamps[0].strftime('%H:%M'))
ax1.set_ylim(20, 25)

# Humidity chart
ax2 = plt.subplot(gs[0:2, 2:4])
ax2.plot([t.strftime('%H:%M') for t in timestamps[::2]], humidity[::2], 'b-', linewidth=2)
ax2.set_title('Humidity (%)', color='white')
ax2.set_facecolor('#1e1e1e')
ax2.grid(color='#333333', linestyle='-', linewidth=0.5)
ax2.tick_params(colors='#8a8a8a')
ax2.set_xlim(timestamps[-1].strftime('%H:%M'), timestamps[0].strftime('%H:%M'))
ax2.set_ylim(35, 55)

# Sensor status indicators
ax3 = plt.subplot(gs[2, 0:2])
ax3.set_title('Sensor Status', color='white')
ax3.set_facecolor('#1e1e1e')
ax3.axis('off')

statuses = [
    ('Living Room Temp', 'ONLINE', 'green'),
    ('Kitchen Humidity', 'ONLINE', 'green'),
    ('Basement Motion', 'OFFLINE', 'red'),
    ('Garden Light', 'ONLINE', 'green')
]

for i, (device, status, color) in enumerate(statuses):
    ax3.text(0.1, 0.8 - i*0.2, device, color='white')
    ax3.text(0.6, 0.8 - i*0.2, status, color=color)

# Alert notifications panel
ax4 = plt.subplot(gs[2, 2:4])
ax4.set_title('Recent Alerts', color='white')
ax4.set_facecolor('#1e1e1e')
ax4.axis('off')

alerts = [
    ('19:30', 'High temperature in Living Room', 'warning'),
    ('18:45', 'Motion detected in Garden', 'info'),
    ('17:15', 'Basement Humidity above threshold', 'critical')
]

for i, (time, alert, level) in enumerate(alerts):
    color = {'info': '#5c9eff', 'warning': '#ffcc00', 'critical': '#ff5c5c'}[level]
    ax4.text(0.05, 0.8 - i*0.25, time, color='#8a8a8a')
    ax4.text(0.2, 0.8 - i*0.25, alert, color=color)

# Navigation sidebar (left)
plt.figtext(0.04, 0.7, 'Dashboard', weight='bold', color='white')
plt.figtext(0.04, 0.65, 'Sensors', color='#8a8a8a')
plt.figtext(0.04, 0.6, 'Automations', color='#8a8a8a')
plt.figtext(0.04, 0.55, 'Analytics', color='#8a8a8a')
plt.figtext(0.04, 0.5, 'Settings', color='#8a8a8a')

# Top navigation bar
plt.figtext(0.85, 0.93, 'User: admin', color='#8a8a8a')
plt.figtext(0.95, 0.93, '⚙️', color='white')

# Adjust layout
plt.tight_layout(rect=[0.02, 0, 0.98, 0.92])

# Ensure directory exists
os.makedirs('docs/images', exist_ok=True)

# Save the image
plt.savefig('docs/images/dashboard_preview.png', dpi=100, bbox_inches='tight')
plt.close()

print("Dashboard preview image created at docs/images/dashboard_preview.png")

