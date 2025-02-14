# HTTP/2 Frame Definitions Guide

## Common Frame Properties
All frames can include these base properties:
- **type**: (Required) The frame type identifier
- **stream_id**: Default varies by frame type
- **flags**: Object containing boolean flag settings
- **raw_frame**: Boolean to bypass h2 validation

## Frame Types and Default Values

### HEADERS Frame
```python
{
    "type": "HEADERS",
    "stream_id": 1,  # Default
    "headers": {  # Defaults if not specified
        ":method": "GET",
        ":path": "/",
        ":authority": "localhost",
        ":scheme": "http"
    },
    "flags": {
        "END_STREAM": True,  # Default
        "END_HEADERS": True  # Default
    }
}
```

### DATA Frame
```python
{
    "type": "DATA",
    "stream_id": 1,  # Default
    "payload": "test",  # Default if payload_size not specified
    "payload_size": None,  # Optional: generates payload of specified size
    "flags": {
        "END_STREAM": True  # Default
    }
}
```

### SETTINGS Frame
```python
{
    "type": "SETTINGS",
    "stream_id": 0,  # Must be 0
    "settings": {},  # No default settings
    "flags": {
        "ACK": False  # Default
    }
}
```

### RST_STREAM Frame
```python
{
    "type": "RST_STREAM",
    "stream_id": 1,  # Default
    "error_code": 0  # Default
}
```

### PRIORITY Frame
```python
{
    "type": "PRIORITY",
    "stream_id": 1,  # Default
    "weight": 15,  # Default
    "depends_on": 0,  # Default
    "exclusive": False  # Default
}
```

### PUSH_PROMISE Frame
```python
{
    "type": "PUSH_PROMISE",
    "stream_id": 1,  # Default
    "promised_stream_id": 2,  # Default
    "headers": {  # Defaults if not specified
        ":status": "200"
    },
    "flags": {
        "END_HEADERS": True,  # Default
        "END_STREAM": True  # Default
    }
}
```

### PING Frame
```python
{
    "type": "PING",
    "stream_id": 0,  # Must be 0
    "data": "\x00\x00\x00\x00\x00\x00\x00\x00",  # Default: 8 zero bytes
    "flags": {
        "ACK": False  # Default
    }
}
```

### WINDOW_UPDATE Frame
```python
{
    "type": "WINDOW_UPDATE",
    "stream_id": 0,  # Default (connection-level)
    "increment": 1024  # Default
}
```

### GOAWAY Frame
```python
{
    "type": "GOAWAY",
    "stream_id": 0,  # Must be 0
    "last_stream_id": 0,  # Default
    "error_code": 0  # Default
}
```

### CONTINUATION Frame
```python
{
    "type": "CONTINUATION",
    "stream_id": None,  # Required (must match preceding HEADERS/PUSH_PROMISE)
    "headers": {  # Defaults if not specified
        "accept-encoding": "gzip, deflate, br"
    },
    "flags": {
        "END_HEADERS": True  # Default
    }
}
```

### TRAILERS Frame
```python
{
    "type": "TRAILERS",
    "stream_id": 1,  # Default
    "headers": {  # Defaults if not specified
        "content-type": "text/plain"
    },
    "flags": {
        "END_STREAM": True  # Default
    }
}
```

### UNKNOWN Frame
```python
{
    "type": "UNKNOWN",
    "stream_id": None,  # Required
    "frame_type_id": None,  # Required
    "payload": "",  # Default
    "flags": []  # Default
}
```
