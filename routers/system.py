from fastapi import APIRouter
import state
from models import CodecFormatBody, VideoFormatBody, SystemFormatBody

router = APIRouter(prefix="/system", tags=["system"])

SUPPORTED_CODECS = [
    {"codec": "ProRes:HQ", "container": "MOV"},
    {"codec": "ProRes:422", "container": "MOV"},
    {"codec": "ProRes:LT", "container": "MOV"},
    {"codec": "ProRes:Proxy", "container": "MOV"},
    {"codec": "BRAW:Q0", "container": "BRAW"},
    {"codec": "BRAW:Q1", "container": "BRAW"},
    {"codec": "BRAW:Q3", "container": "BRAW"},
    {"codec": "BRAW:Q5", "container": "BRAW"},
]

SUPPORTED_VIDEO_FORMATS = [
    {"name": "1920x1080p23.98", "frameRate": "23.98", "height": 1080, "width": 1920, "interlaced": False},
    {"name": "1920x1080p24",    "frameRate": "24",    "height": 1080, "width": 1920, "interlaced": False},
    {"name": "1920x1080p25",    "frameRate": "25",    "height": 1080, "width": 1920, "interlaced": False},
    {"name": "1920x1080p29.97", "frameRate": "29.97", "height": 1080, "width": 1920, "interlaced": False},
    {"name": "1920x1080p30",    "frameRate": "30",    "height": 1080, "width": 1920, "interlaced": False},
    {"name": "1920x1080p50",    "frameRate": "50",    "height": 1080, "width": 1920, "interlaced": False},
    {"name": "1920x1080p59.94", "frameRate": "59.94", "height": 1080, "width": 1920, "interlaced": False},
    {"name": "1920x1080p60",    "frameRate": "60",    "height": 1080, "width": 1920, "interlaced": False},
    {"name": "3840x2160p23.98", "frameRate": "23.98", "height": 2160, "width": 3840, "interlaced": False},
    {"name": "3840x2160p24",    "frameRate": "24",    "height": 2160, "width": 3840, "interlaced": False},
    {"name": "3840x2160p25",    "frameRate": "25",    "height": 2160, "width": 3840, "interlaced": False},
    {"name": "3840x2160p29.97", "frameRate": "29.97", "height": 2160, "width": 3840, "interlaced": False},
    {"name": "3840x2160p30",    "frameRate": "30",    "height": 2160, "width": 3840, "interlaced": False},
]

FRAME_RATES = ["23.98", "24", "25", "29.97", "30", "47.95", "48", "50", "59.94", "60"]


@router.get("")
def get_system():
    c = state.state.camera
    return {
        "codecFormat": {"codec": c.codec, "container": c.container},
        "videoFormat": {
            "name": c.video_format_name,
            "frameRate": c.video_frame_rate,
            "height": c.video_height,
            "width": c.video_width,
            "interlaced": c.video_interlaced,
        },
    }


@router.get("/product")
def get_product():
    c = state.state.camera
    return {
        "deviceName": c.device_name,
        "productName": c.product_name,
        "softwareVersion": c.software_version,
    }


@router.get("/codecFormat")
def get_codec_format():
    c = state.state.camera
    return {"codec": c.codec, "container": c.container}


@router.put("/codecFormat")
def set_codec_format(body: CodecFormatBody):
    c = state.state.camera
    c.codec = body.codec
    c.container = body.container
    return {}


@router.get("/supportedCodecFormats")
def get_supported_codec_formats():
    return {"codecs": SUPPORTED_CODECS}


@router.get("/videoFormat")
def get_video_format():
    c = state.state.camera
    return {
        "name": c.video_format_name,
        "frameRate": c.video_frame_rate,
        "height": c.video_height,
        "width": c.video_width,
        "interlaced": c.video_interlaced,
    }


@router.put("/videoFormat")
def set_video_format(body: VideoFormatBody):
    c = state.state.camera
    if body.name is not None:
        c.video_format_name = body.name
    if body.frameRate is not None:
        c.video_frame_rate = body.frameRate
    if body.height is not None:
        c.video_height = body.height
    if body.width is not None:
        c.video_width = body.width
    if body.interlaced is not None:
        c.video_interlaced = body.interlaced
    return {}


@router.get("/supportedVideoFormats")
def get_supported_video_formats():
    return {"formats": SUPPORTED_VIDEO_FORMATS}


@router.get("/supportedFormats")
def get_supported_formats():
    return {
        "supportedFormats": [
            {
                "codecs": [c["codec"] for c in SUPPORTED_CODECS],
                "frameRates": FRAME_RATES,
                "maxOffSpeedFrameRate": 120,
                "minOffSpeedFrameRate": 1,
                "recordResolution": {"width": 1920, "height": 1080},
                "sensorResolution": {"width": 1920, "height": 1080},
            },
            {
                "codecs": [c["codec"] for c in SUPPORTED_CODECS],
                "frameRates": FRAME_RATES,
                "maxOffSpeedFrameRate": 60,
                "minOffSpeedFrameRate": 1,
                "recordResolution": {"width": 3840, "height": 2160},
                "sensorResolution": {"width": 3840, "height": 2160},
            },
        ]
    }


@router.get("/format")
def get_format():
    c = state.state.camera
    return {
        "codec": c.codec,
        "frameRate": c.format_frame_rate,
        "maxOffSpeedFrameRate": 120,
        "minOffSpeedFrameRate": 1,
        "offSpeedEnabled": c.off_speed_enabled,
        "offSpeedFrameRate": c.off_speed_frame_rate,
        "recordResolution": {"width": c.record_resolution_width, "height": c.record_resolution_height},
        "sensorResolution": {"width": c.sensor_resolution_width, "height": c.sensor_resolution_height},
    }


@router.put("/format")
def set_format(body: SystemFormatBody):
    c = state.state.camera
    if body.codec is not None:
        c.codec = body.codec
    if body.frameRate is not None:
        c.format_frame_rate = body.frameRate
    if body.offSpeedEnabled is not None:
        c.off_speed_enabled = body.offSpeedEnabled
    if body.offSpeedFrameRate is not None:
        c.off_speed_frame_rate = body.offSpeedFrameRate
    if body.recordResolution is not None:
        c.record_resolution_width = body.recordResolution.get("width", c.record_resolution_width)
        c.record_resolution_height = body.recordResolution.get("height", c.record_resolution_height)
    if body.sensorResolution is not None:
        c.sensor_resolution_width = body.sensorResolution.get("width", c.sensor_resolution_width)
        c.sensor_resolution_height = body.sensorResolution.get("height", c.sensor_resolution_height)
    return {}
