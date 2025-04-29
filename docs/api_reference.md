# API Reference

## Overview

SmartSense provides a comprehensive RESTful API that allows you to integrate with and extend the platform. This document outlines the available endpoints, authentication methods, and response formats.

## Authentication

All API requests require authentication using one of the following methods:

### API Key Authentication

Include your API key in the request header:

```
Authorization: ApiKey your-api-key-here
```

### OAuth 2.0

SmartSense supports OAuth 2.0 for secure third-party application access. To use OAuth:

1. Register your application in the SmartSense dashboard under Settings > API Access
2. Implement the OAuth 2.0 authorization flow
3. Use the obtained bearer token in your requests:

```
Authorization: Bearer your-bearer-token-here
```

## Base URL

All API endpoints are relative to your SmartSense instance:

```
https://your-smartsense-instance.com/api/v1/
```

## Response Format

All responses are returned in JSON format with the following structure:

```json
{
  "status": "success",  // or "error"
  "data": {             // Contains the response data (null if error)
    // Response-specific fields
  },
  "error": {            // Present only if status is "error"
    "code": "ERROR_CODE",
    "message": "Human-readable error message"
  },
  "pagination": {       // Present only for paginated responses
    "page": 1,
    "per_page": 25,
    "total_pages": 4,
    "total_items": 96
  }
}
```

## Rate Limiting

API requests are rate-limited to prevent abuse. The current limits are:

- 100 requests per minute for regular API keys
- 1000 requests per minute for premium API keys

Rate limit information is included in response headers:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1619642123
```

## API Endpoints

### Sensors

#### GET /sensors

Returns a list of all sensors.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| type | string | Filter by sensor type (e.g., "temperature", "humidity") |
| status | string | Filter by status (e.g., "online", "offline") |
| page | integer | Page number for pagination (default: 1) |
| per_page | integer | Items per page (default: 25, max: 100) |

**Response:**

```json
{
  "status": "success",
  "data": [
    {
      "id": "sensor-uuid-here",
      "name": "Living Room Temperature",
      "type": "temperature",
      "status": "online",
      "last_reading": {
        "value": 22.5,
        "unit": "celsius",
        "timestamp": "2025-04-29T14:32:10Z"
      },
      "metadata": {
        "location": "living_room",
        "floor": 1
      }
    },
    // More sensors...
  ],
  "pagination": {
    "page": 1,
    "per_page": 25,
    "total_pages": 2,
    "total_items": 36
  }
}
```

#### GET /sensors/{sensor_id}

Returns detailed information about a specific sensor.

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": "sensor-uuid-here",
    "name": "Living Room Temperature",
    "type": "temperature",
    "model": "SmartSense-T100",
    "firmware": "1.2.3",
    "status": "online",
    "last_reading": {
      "value": 22.5,
      "unit": "celsius",
      "timestamp": "2025-04-29T14:32:10Z"
    },
    "metadata": {
      "location": "living_room",
      "floor": 1,
      "installation_date": "2025-01-15"
    },
    "configuration": {
      "update_interval": 60,
      "threshold_high": 26.0,
      "threshold_low": 18.0
    }
  }
}
```

#### POST /sensors

Creates a new sensor.

**Request Body:**

```json
{
  "name": "Kitchen Humidity",
  "type": "humidity",
  "model": "SmartSense-H200",
  "metadata": {
    "location": "kitchen",
    "floor": 1
  },
  "configuration": {
    "update_interval": 120,
    "threshold_high": 65.0,
    "threshold_low": 30.0
  }
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": "newly-created-sensor-uuid",
    "name": "Kitchen Humidity",
    "type": "humidity",
    "model": "SmartSense-H200",
    "status": "initializing",
    "metadata": {
      "location": "kitchen",
      "floor": 1
    },
    "configuration": {
      "update_interval": 120,
      "threshold_high": 65.0,
      "threshold_low": 30.0
    }
  }
}
```

#### PUT /sensors/{sensor_id}

Updates an existing sensor.

**Request Body:**

```json
{
  "name": "Updated Sensor Name",
  "configuration": {
    "update_interval": 30
  }
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": "sensor-uuid-here",
    "name": "Updated Sensor Name",
    "type": "temperature",
    "model": "SmartSense-T100",
    "status": "online",
    "configuration": {
      "update_interval": 30,
      "threshold_high": 26.0,
      "threshold_low": 18.0
    },
    // Other unchanged fields...
  }
}
```

#### DELETE /sensors/{sensor_id}

Removes a sensor from the system.

**Response:**

```json
{
  "status": "success",
  "data": {
    "message": "Sensor successfully deleted"
  }
}
```

### Readings

#### GET /readings

Returns sensor readings.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| sensor_id | string | Filter by sensor ID |
| type | string | Filter by reading type (e.g., "temperature") |
| from | string | Start timestamp (ISO 8601) |
| to | string | End timestamp (ISO 8601) |
| interval | string | Aggregation interval (e.g., "1h", "1d") |
| page | integer | Page number for pagination |
| per_page | integer | Items per page |

**Response:**

```json
{
  "status": "success",
  "data": [
    {
      "sensor_id": "sensor-uuid-here",
      "type": "temperature",
      "value": 22.5,
      "unit": "celsius",
      "timestamp": "2025-04-29T14:00:00Z"
    },
    {
      "sensor_id": "sensor-uuid-here",
      "type": "temperature",
      "value": 22.8,
      "unit": "celsius", 
      "timestamp": "2025-04-29T14:15:00Z"
    },
    // More readings...
  ],
  "pagination": {
    "page": 1,
    "per_page": 25,
    "total_pages": 10,
    "total_items": 240
  }
}
```

### Alerts

#### GET /alerts

Returns a list of alerts.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| sensor_id | string | Filter by sensor ID |
| status | string | Filter by status (e.g., "active", "resolved") |
| severity | string | Filter by severity (e.g., "low", "medium", "high") |
| page | integer | Page number for pagination |
| per_page | integer | Items per page |

**Response:**

```json
{
  "status": "success",
  "data": [
    {
      "id": "alert-uuid-here",
      "sensor_id": "sensor-uuid-here",
      "type": "threshold_exceeded",
      "message": "Temperature above threshold: 28.5°C (Threshold: 26.0°C)",
      "severity": "high",
      "status": "active",
      "created_at": "2025-04-29T15:20:00Z",
      "updated_at": "2025-04-29T15:20:00Z"
    },
    // More alerts...
  ],
  "pagination": {
    "page": 1,
    "per_page": 25,
    "total_pages": 1,
    "total_items": 5
  }
}
```

#### POST /alerts

Creates a new alert configuration.

**Request Body:**

```json
{
  "name": "High Temperature Alert",
  "sensor_id": "sensor-uuid-here",
  "condition": {
    "field": "temperature",
    "operator": "gt",
    "value": 28.0
  },
  "severity": "high",
  "actions": [
    {
      "type": "notification",
      "config": {
        "channels": ["email", "sms"],
        "recipients": ["user@example.com", "+12345678901"]
      }
    },
    {
      "type": "webhook",
      "config": {
        "url": "https://example.com/webhook",
        "method": "POST"
      }
    }
  ]
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": "alert-config-uuid-here",
    "name": "High Temperature Alert",
    "sensor_id": "sensor-uuid-here",
    "condition": {
      "field": "temperature",
      "operator": "gt",
      "value": 28.0
    },
    "severity": "high",
    "actions": [
      {
        "type": "notification",
        "config": {
          "channels": ["email", "sms"],
          "recipients": ["user@example.com", "+12345678901"]
        }
      },
      {
        "type": "webhook",
        "config": {
          "url": "https://example.com/webhook",
          "method": "POST"
        }
      }
    ],
    "created_at": "2025-04-29T15:20:00Z",
    "updated_at": "2025-04-29T15:20:00Z"
  }
}
```

### Dashboards

#### GET /dashboards

Returns a list of available dashboards.

**Response:**

```json
{
  "status": "success",
  "data": [
    {
      "id": "dashboard-uuid-here",
      "name": "Home Environment",
      "description": "Overview of home temperature and humidity",
      "created_at": "2025-03-15T10:00:00Z",
      "updated_at": "2025-04-20T14:30:00Z"
    },
    // More dashboards...
  ]
}
```

#### GET /dashboards/{dashboard_id}

Returns a specific dashboard configuration including widgets.

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": "dashboard-uuid-here",
    "name": "Home Environment",
    "description": "Overview of home temperature and humidity",
    "layout": "grid",
    "widgets": [
      {
        "id": "widget-uuid-1",
        "type": "chart",
        "title": "Living Room Temperature",
        "position": {"x": 0, "y": 0, "w": 6, "h": 4},
        "config": {
          "sensor_id": "living-room-temp-sensor-id",
          "chart_type": "line",
          "time_range": "24h"
        }
      },
      {
        "id": "widget-uuid-2",
        "type": "gauge",
        "title": "Kitchen Humidity",
        "position": {"x": 6, "y": 0, "w": 3, "h": 4},
        "config": {
          "sensor_id": "kitchen-humidity-sensor-id",
          "min": 0,
          "max": 100,
          "thresholds": [
            {"value": 30, "color": "#3498db"},
            {"value": 60, "color": "#2ecc71"},
            {"value": 80, "color": "#f39c12"}
          ]
        }
      }
      // More widgets...
    ],
    "created_at": "2025-03-15T10:00:00Z",
    "updated_at": "2025-04-20T14:30:00Z"
  }
}
```

## Webhook Integrations

SmartSense can send webhook notifications for various events. Configure webhooks in the dashboard under Settings > Integrations > Webhooks.

### Webhook Payload Format

```json
{
  "event": "sensor.reading.threshold_exceeded",
  "timestamp": "2025-04-29T15:20:00Z",
  "data": {
    "sensor_id": "sensor-uuid-here",
    "sensor_name": "Living Room Temperature",
    "reading": {
      "type": "temperature",
      "value": 28.5,
      "unit": "celsius",
      "timestamp": "2025-04-29T15:20:00Z"
    },
    "threshold": {
      "type": "high",
      "value": 26.0
    }
  }
}
```

### Available Webhook Events

| Event | Description |
|-------|-------------|
| sensor.reading.new | Triggered when a new sensor reading is recorded |
| sensor.reading.threshold_exceeded | Triggered when a reading exceeds a threshold |
| sensor.status.changed | Triggered when a sensor's status changes |
| alert.triggered | Triggered when a new alert is generated |
| alert.resolved | Triggered when an alert is resolved |
| system.status.changed | Triggered when the system status changes |

## Error Codes

| Code | Description |
|------|-------------|
| AUTH_REQUIRED | Authentication is required |
| INVALID_API_KEY | API key is invalid or expired |
| RATE_LIMIT_EXCEEDED | API rate limit exceeded |
| RESOURCE_NOT_FOUND | Requested resource not found |
| VALIDATION_ERROR | Invalid request parameters |
| INTERNAL_ERROR | Internal server error |

## API Client Libraries

SmartSense provides official client libraries for popular programming languages:

- Python: [smartsense-python](https://github.com/aaronjacobs-chelt/smartsense-python)
- JavaScript: [smartsense-js](https://github.com/aaronjacobs-chelt/smartsense-js) 
- Java: [smartsense-java](https://github.com/aaronjacobs-chelt/smartsense-java)

## API Versioning

The SmartSense API uses semantic versioning. The current version is v1. When breaking changes are introduced, a new version will be released, and the previous version will be maintained for a deprecation period of at least 12 months.

## Batch Operations

SmartSense API supports batch operations to reduce the number of API calls for multiple operations.

### POST /batch

Executes multiple API operations in a single request.

**Request Body:**

```json
{
  "operations": [
    {
      "method": "GET",
      "path":

# API Reference

## Overview

SmartSense provides a comprehensive RESTful API that allows you to integrate with and extend the platform. This document outlines the available endpoints, authentication methods, and response formats.

## Authentication

All API requests require authentication using one of the following methods:

### API Key Authentication

Include your API key in the request header:

```
Authorization: ApiKey your-api-key-here
```

### OAuth 2.0

SmartSense supports OAuth 2.0 for secure third-party application access. To use OAuth:

1. Register your application in the SmartSense dashboard under Settings > API Access
2. Implement the OAuth 2.0 authorization flow
3. Use the obtained bearer token in your requests:

```
Authorization: Bearer your-bearer-token-here
```

## Base URL

All API endpoints are relative to your SmartSense instance:

```
https://your-smartsense-instance.com/api/v1/
```

## Response Format

All responses are returned in JSON format with the following structure:

```json
{
  "status": "success",  // or "error"
  "data": {             // Contains the response data (null if error)
    // Response-specific fields
  },
  "error": {            // Present only if status is "error"
    "code": "ERROR_CODE",
    "message": "Human-readable error message"
  },
  "pagination": {       // Present only for paginated responses
    "page": 1,
    "per_page": 25,
    "total_pages": 4,
    "total_items": 96
  }
}
```

## Rate Limiting

API requests are rate-limited to prevent abuse. The current limits are:

- 100 requests per minute for regular API keys
- 1000 requests per minute for premium API keys

Rate limit information is included in response headers:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1619642123
```

## API Endpoints

### Sensors

#### GET /sensors

Returns a list of all sensors.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| type | string | Filter by sensor type (e.g., "temperature", "humidity") |
| status | string | Filter by status (e.g., "online", "offline") |
| page | integer | Page number for pagination (default: 1) |
| per_page | integer | Items per page (default: 25, max: 100) |

**Response:**

```json
{
  "status": "success",
  "data": [
    {
      "id": "sensor-uuid-here",
      "name": "Living Room Temperature",
      "type": "temperature",
      "status": "online",
      "last_reading": {
        "value": 22.5,
        "unit": "celsius",
        "timestamp": "2025-04-29T14:32:10Z"
      },
      "metadata": {
        "location": "living_room",
        "floor": 1
      }
    },
    // More sensors...
  ],
  "pagination": {
    "page": 1,
    "per_page": 25,
    "total_pages": 2,
    "total_items": 36
  }
}
```

#### GET /sensors/{sensor_id}

Returns detailed information about a specific sensor.

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": "sensor-uuid-here",
    "name": "Living Room Temperature",
    "type": "temperature",
    "model": "SmartSense-T100",
    "firmware": "1.2.3",
    "status": "online",
    "last_reading": {
      "value": 22.5,
      "unit": "celsius",
      "timestamp": "2025-04-29T14:32:10Z"
    },
    "metadata": {
      "location": "living_room",
      "floor": 1,
      "installation_date": "2025-01-15"
    },
    "configuration": {
      "update_interval": 60,
      "threshold_high": 26.0,
      "threshold_low": 18.0
    }
  }
}
```

#### POST /sensors

Creates a new sensor.

**Request Body:**

```json
{
  "name": "Kitchen Humidity",
  "type": "humidity",
  "model": "SmartSense-H200",
  "metadata": {
    "location": "kitchen",
    "floor": 1
  },
  "configuration": {
    "update_interval": 120,
    "threshold_high": 65.0,
    "threshold_low": 30.0
  }
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": "newly-created-sensor-uuid",
    "name": "Kitchen Humidity",
    "type": "humidity",
    "model": "SmartSense-H200",
    "status": "initializing",
    "metadata": {
      "location": "kitchen",
      "floor": 1
    },
    "configuration": {
      "update_interval": 120,
      "threshold_high": 65.0,
      "threshold_low": 30.0
    }
  }
}
```

#### PUT /sensors/{sensor_id}

Updates an existing sensor.

**Request Body:**

```json
{
  "name": "Updated Sensor Name",
  "configuration": {
    "update_interval": 30
  }
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": "sensor-uuid-here",
    "name": "Updated Sensor Name",
    "type": "temperature",
    "model": "SmartSense-T100",
    "status": "online",
    "configuration": {
      "update_interval": 30,
      "threshold_high": 26.0,
      "threshold_low": 18.0
    },
    // Other unchanged fields...
  }
}
```

#### DELETE /sensors/{sensor_id}

Removes a sensor from the system.

**Response:**

```json
{
  "status": "success",
  "data": {
    "message": "Sensor successfully deleted"
  }
}
```

### Readings

#### GET /readings

Returns sensor readings.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| sensor_id | string | Filter by sensor ID |
| type | string | Filter by reading type (e.g., "temperature") |
| from | string | Start timestamp (ISO 8601) |
| to | string | End timestamp (ISO 8601) |
| interval | string | Aggregation interval (e.g., "1h", "1d") |
| page | integer | Page number for pagination |
| per_page | integer | Items per page |

**Response:**

```json
{
  "status": "success",
  "data": [
    {
      "sensor_id": "sensor-uuid-here",
      "type": "temperature",
      "value": 22.5,
      "unit": "celsius",
      "timestamp": "2025-04-29T14:00:00Z"
    },
    {
      "sensor_id": "sensor-uuid-here",
      "type": "temperature",
      "value": 22.8,
      "unit": "celsius", 
      "timestamp": "2025-04-29T14:15:00Z"
    },
    // More readings...
  ],
  "pagination": {
    "page": 1,
    "per_page": 25,
    "total_pages": 10,
    "total_items": 240
  }
}
```

### Alerts

#### GET /alerts

Returns a list of alerts.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| sensor_id | string | Filter by sensor ID |
| status | string | Filter by status (e.g., "active", "resolved") |
| severity | string | Filter by severity (e.g., "low", "medium", "high") |
| page | integer | Page number for pagination |
| per_page | integer | Items per page |

**Response:**

```json
{
  "status": "success",
  "data": [
    {
      "id": "alert-uuid-here",
      "sensor_id": "sensor-uuid-here",
      "type": "threshold_exceeded",
      "message": "Temperature above threshold: 28.5°C (Threshold: 26.0°C)",
      "severity": "high",
      "status": "active",
      "created_at": "2025-04-29T15:20:00Z",
      "updated_at": "2025-04-29T15:20:00Z"
    },
    // More alerts...
  ],
  "pagination": {
    "page": 1,
    "per_page": 25,
    "total_pages": 1,
    "total_items": 5
  }
}
```

## Webhook Integrations

SmartSense can send webhook notifications for various events. Configure webhooks in the dashboard under Settings > Integrations > Webhooks.

### Webhook Payload Format

```json
{
  "event": "sensor.reading.threshold_exceeded",
  "timestamp": "2025-04-29T15:20:00Z",
  "data": {
    "sensor_id": "sensor-uuid-here",
    "sensor_name": "Living Room Temperature",
    "reading": {
      "type": "temperature",
      "value": 28.5,
      "unit": "celsius",
      "timestamp": "2025-04-29T15:20:00Z"
    },
    "threshold": {
      "type": "high",
      "value": 26.0
    }
  }
}
```

## Error Codes

| Code | Description |
|------|-------------|
| AUTH_REQUIRED | Authentication is required |
| INVALID_API_KEY | API key is invalid or expired |
| RATE_LIMIT_EXCEEDED | API rate limit exceeded |
| RESOURCE_NOT_FOUND | Requested resource not found |
| VALIDATION_ERROR | Invalid request parameters |
| INTERNAL_ERROR | Internal server error |

## API Client Libraries

SmartSense provides official client libraries for popular programming languages:

- Python: [smartsense-python](https://github.com/aaronjacobs-chelt/smartsense-python)
- JavaScript: [smartsense-js](https://github.com/aaronjacobs-chelt/smartsense-js) 
- Java: [smartsense-java](https://github.com/aaronjacobs-chelt/smartsense-java)

## API Versioning

The SmartSense API uses semantic versioning. The current version is v1. When breaking changes are introduced, a new version will be released, and the previous version will be maintained for a deprecation period of at least 12 months.

