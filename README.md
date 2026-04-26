# Blackmagic Camera Control API Emulator

A FastAPI server that mimics the REST API exposed by Blackmagic Design cameras, for development and testing without physical hardware.

## Prerequisites

- Python 3.10+

## Installation

```bash
pip install -r requirements.txt
```

## Starting the Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

| URL | Description |
|-----|-------------|
| `http://localhost:8080/control/api/v1` | API base URL |
| `http://localhost:8080/docs` | Interactive API documentation (Swagger UI) |

### Reset all state to defaults

```bash
curl -X POST http://localhost:8080/reset
```

---

## Example curl Commands

All endpoints below are relative to `http://localhost:8080/control/api/v1`.

### System

```bash
# Get camera product info
curl http://localhost:8080/control/api/v1/system/product

# Get current video format
curl http://localhost:8080/control/api/v1/system/videoFormat

# Set video format
curl -X PUT http://localhost:8080/control/api/v1/system/videoFormat \
  -H "Content-Type: application/json" \
  -d '{"frameRate": "25", "height": 2160, "width": 3840, "interlaced": false}'

# Get supported codec formats
curl http://localhost:8080/control/api/v1/system/supportedCodecFormats

# Set codec format
curl -X PUT http://localhost:8080/control/api/v1/system/codecFormat \
  -H "Content-Type: application/json" \
  -d '{"codec": "ProRes:HQ", "container": "MOV"}'
```

### Video

```bash
# Get current ISO
curl http://localhost:8080/control/api/v1/video/iso

# Set ISO
curl -X PUT http://localhost:8080/control/api/v1/video/iso \
  -H "Content-Type: application/json" \
  -d '{"iso": 800}'

# Get supported ISO values
curl http://localhost:8080/control/api/v1/video/supportedISOs

# Set white balance
curl -X PUT http://localhost:8080/control/api/v1/video/whiteBalance \
  -H "Content-Type: application/json" \
  -d '{"whiteBalance": 5600}'

# Trigger auto white balance
curl -X PUT http://localhost:8080/control/api/v1/video/whiteBalance/doAuto

# Set shutter angle
curl -X PUT http://localhost:8080/control/api/v1/video/shutter \
  -H "Content-Type: application/json" \
  -d '{"shutterAngle": 18000}'

# Set ND filter
curl -X PUT http://localhost:8080/control/api/v1/video/ndFilter \
  -H "Content-Type: application/json" \
  -d '{"stop": 2.0}'

# Set auto exposure mode
curl -X PUT http://localhost:8080/control/api/v1/video/autoExposure \
  -H "Content-Type: application/json" \
  -d '{"mode": "Continuous", "type": "Iris"}'
```

### Lens

```bash
# Get iris/aperture
curl http://localhost:8080/control/api/v1/lens/iris

# Set iris
curl -X PUT http://localhost:8080/control/api/v1/lens/iris \
  -H "Content-Type: application/json" \
  -d '{"apertureStop": 2.8}'

# Get focus
curl http://localhost:8080/control/api/v1/lens/focus

# Set focus (normalised 0.0–1.0)
curl -X PUT http://localhost:8080/control/api/v1/lens/focus \
  -H "Content-Type: application/json" \
  -d '{"normalised": 0.5}'

# Trigger auto focus
curl -X PUT http://localhost:8080/control/api/v1/lens/focus/doAutoFocus

# Set zoom (focal length in mm)
curl -X PUT http://localhost:8080/control/api/v1/lens/zoom \
  -H "Content-Type: application/json" \
  -d '{"focalLength": 50}'
```

### Transport

```bash
# Get transport mode
curl http://localhost:8080/control/api/v1/transports/0

# Set transport mode
curl -X PUT http://localhost:8080/control/api/v1/transports/0 \
  -H "Content-Type: application/json" \
  -d '{"mode": "InputPreview"}'

# Start recording
curl -X POST http://localhost:8080/control/api/v1/transports/0/record

# Start recording with a clip name
curl -X POST http://localhost:8080/control/api/v1/transports/0/record \
  -H "Content-Type: application/json" \
  -d '{"clipName": "A001C001"}'

# Stop recording/playback
curl -X POST http://localhost:8080/control/api/v1/transports/0/stop

# Start playback
curl -X POST http://localhost:8080/control/api/v1/transports/0/play

# Get timecode
curl http://localhost:8080/control/api/v1/transports/0/timecode
```

### Audio

```bash
# Get all audio channels
curl http://localhost:8080/control/api/v1/audio/channels

# Set channel 0 input type
curl -X PUT http://localhost:8080/control/api/v1/audio/channel/0/input \
  -H "Content-Type: application/json" \
  -d '{"input": "XLR"}'

# Set channel 0 level
curl -X PUT http://localhost:8080/control/api/v1/audio/channel/0/level \
  -H "Content-Type: application/json" \
  -d '{"gain": 0.0}'

# Enable phantom power on channel 0
curl -X PUT http://localhost:8080/control/api/v1/audio/channel/0/phantomPower \
  -H "Content-Type: application/json" \
  -d '{"enabled": true}'

# Enable low cut filter on channel 1
curl -X PUT http://localhost:8080/control/api/v1/audio/channel/1/lowCutFilter \
  -H "Content-Type: application/json" \
  -d '{"enabled": true}'
```

### Color Correction

```bash
# Get lift values
curl http://localhost:8080/control/api/v1/colorCorrection/lift

# Set lift
curl -X PUT http://localhost:8080/control/api/v1/colorCorrection/lift \
  -H "Content-Type: application/json" \
  -d '{"red": 0.0, "green": 0.0, "blue": 0.0, "luma": 0.0}'

# Set gain
curl -X PUT http://localhost:8080/control/api/v1/colorCorrection/gain \
  -H "Content-Type: application/json" \
  -d '{"red": 1.0, "green": 1.0, "blue": 1.0, "luma": 1.0}'

# Set saturation and hue
curl -X PUT http://localhost:8080/control/api/v1/colorCorrection/color \
  -H "Content-Type: application/json" \
  -d '{"hue": 0.0, "saturation": 1.0}'

# Set contrast
curl -X PUT http://localhost:8080/control/api/v1/colorCorrection/contrast \
  -H "Content-Type: application/json" \
  -d '{"pivot": 0.5, "adjust": 1.0}'
```

### Monitoring

```bash
# List displays
curl http://localhost:8080/control/api/v1/monitoring/display

# Enable zebra on main display
curl -X PUT http://localhost:8080/control/api/v1/monitoring/main/zebra \
  -H "Content-Type: application/json" \
  -d '{"enabled": true}'

# Enable false color on main display
curl -X PUT http://localhost:8080/control/api/v1/monitoring/main/falseColor \
  -H "Content-Type: application/json" \
  -d '{"enabled": true}'

# Configure focus assist
curl -X PUT http://localhost:8080/control/api/v1/monitoring/main/focusAssist \
  -H "Content-Type: application/json" \
  -d '{"mode": "Peak", "color": "Red", "intensity": 0.8}'

# Enable clean feed
curl -X PUT http://localhost:8080/control/api/v1/monitoring/main/cleanFeed \
  -H "Content-Type: application/json" \
  -d '{"enabled": true}'
```

### Camera

```bash
# Get tally status
curl http://localhost:8080/control/api/v1/camera/tallyStatus

# Enable color bars
curl -X PUT http://localhost:8080/control/api/v1/camera/colorBars \
  -H "Content-Type: application/json" \
  -d '{"enabled": true}'

# Get battery/power info
curl http://localhost:8080/control/api/v1/camera/power
```

### Slate

```bash
# Get next clip slate info
curl http://localhost:8080/control/api/v1/slates/nextClip

# Set slate metadata
curl -X PUT http://localhost:8080/control/api/v1/slates/nextClip \
  -H "Content-Type: application/json" \
  -d '{
    "clip": {
      "clipName": "A001C001",
      "scene": "42",
      "take": "1",
      "shotType": "WS",
      "goodTake": false
    },
    "project": {
      "projectName": "My Film",
      "director": "Jane Smith",
      "camera": "A"
    }
  }'

# Reset project data on slate
curl -X POST http://localhost:8080/control/api/v1/slates/nextClip/resetProjectData
```

### Media

```bash
# Get working set (list of media devices)
curl http://localhost:8080/control/api/v1/media/workingset

# Get active media device
curl http://localhost:8080/control/api/v1/media/active

# Set active media device by index
curl -X PUT http://localhost:8080/control/api/v1/media/active \
  -H "Content-Type: application/json" \
  -d '{"workingsetIndex": 0}'
```

### Presets

```bash
# List all presets
curl http://localhost:8080/control/api/v1/presets

# Get active preset
curl http://localhost:8080/control/api/v1/presets/active

# Set active preset
curl -X PUT http://localhost:8080/control/api/v1/presets/active \
  -H "Content-Type: application/json" \
  -d '{"preset": "MyPreset"}'

# Save current state as a named preset
curl -X PUT http://localhost:8080/control/api/v1/presets/MyPreset

# Delete a preset
curl -X DELETE http://localhost:8080/control/api/v1/presets/MyPreset
```

---

## Notes

- No authentication is required.
- CORS is open to all origins, making it suitable for testing from browser-based or mobile apps on the same network.
- All camera state is held in memory and lost when the server restarts. Use `POST /reset` to return to defaults without restarting.
