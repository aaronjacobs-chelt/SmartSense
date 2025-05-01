# Troubleshooting Guide

## Version: 1.0.0 (May 2025)

This guide helps you diagnose and resolve common issues with SmartSense.

## Common Issues

### Installation Problems

#### Package Installation Fails
```
Problem: pip install fails
Solution: 
1. Ensure Python 3.9+ is installed
2. Update pip: pip install --upgrade pip
3. Check system requirements
```

#### Import Errors
```
Problem: Import errors after installation
Solution:
1. Verify virtual environment is activated
2. Confirm installation: pip list | grep smartsense
3. Reinstall if necessary
```

### Sensor Issues

#### Sensor Not Detected
```
Problem: Sensor not showing in network
Solution:
1. Check physical connections
2. Verify sensor configuration
3. Check logs for errors
```

#### Incorrect Readings
```
Problem: Sensor readings seem wrong
Solution:
1. Calibrate sensor
2. Check sensor placement
3. Verify power supply
```

### Network Issues

#### Connection Failures
```
Problem: Network won't start
Solution:
1. Check network configuration
2. Verify permissions
3. Review firewall settings
```

#### Data Loss
```
Problem: Missing sensor data
Solution:
1. Check network stability
2. Verify storage configuration
3. Review buffer settings
```

## Logging

### Log Locations
- Application logs: /var/log/smartsense/
- Debug logs: /var/log/smartsense/debug/
- Error logs: /var/log/smartsense/error/

### Enabling Debug Logging
```python
import logging
logging.getLogger('smartsense').setLevel(logging.DEBUG)
```

### Common Log Messages

#### ERROR: Failed to initialize sensor
```
Cause: Sensor configuration or connection issue
Solution: Check sensor setup and permissions
```

#### WARNING: Network buffer full
```
Cause: Data processing bottleneck
Solution: Adjust buffer size or processing rate
```

## Diagnostics

### System Health Check
```bash
smartsense-cli diagnose
```

### Configuration Validation
```bash
smartsense-cli validate-config
```

### Network Testing
```bash
smartsense-cli test-network
```

## Getting Help

If you can't resolve an issue:

1. Check our [FAQ](faq.md)
2. Search [GitHub Issues](https://github.com/aaronjacobs-chelt/SmartSense/issues)
3. Start a [Discussion](https://github.com/aaronjacobs-chelt/SmartSense/discussions)
4. Email support: git@happycaps.co.uk

## Debug Mode

Enable debug mode for detailed logging:

```python
from smartsense import SensorNetwork
network = SensorNetwork(name="Debug Network", debug=True)
```

## Common Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| E001 | Sensor initialization failed | Check connections and power |
| E002 | Network configuration error | Verify network settings |
| E003 | Data storage error | Check disk space and permissions |
| E004 | Alert system failure | Review alert configuration |

## Reporting Issues

When reporting issues:

1. Include error messages
2. Provide system information
3. List steps to reproduce
4. Attach relevant logs
5. Describe expected behavior

---

Last updated: May 1, 2025
