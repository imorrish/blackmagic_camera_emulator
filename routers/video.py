from fastapi import APIRouter
import state
from models import (
    IsoBody, GainBody, WhiteBalanceBody, WhiteBalanceTintBody,
    NDFilterBody, NDFilterDisplayModeBody, ShutterBody, ShutterMeasurementBody,
    AutoExposureBody, DetailSharpeningBody, DetailSharpeningLevelBody,
)

router = APIRouter(prefix="/video", tags=["video"])

# Realistic URSA Mini Pro capabilities
SUPPORTED_ISOS = [100, 125, 160, 200, 250, 320, 400, 500, 640, 800, 1000, 1250, 1600,
                  2000, 2500, 3200, 4000, 5000, 6400, 12800, 25600]
SUPPORTED_GAINS = list(range(-12, 37, 6))  # dB steps
SUPPORTED_ND_STOPS = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0]
SUPPORTED_SHUTTER_ANGLES = [11, 15, 17, 22, 30, 45, 60, 72, 90, 120, 144, 150, 172, 180,
                             270, 360]
SUPPORTED_SHUTTER_SPEEDS = [25, 30, 40, 48, 50, 60, 75, 90, 100, 120, 125, 150, 180, 250,
                              500, 1000, 2000]


# ---------------------------------------------------------------------------
# ISO
# ---------------------------------------------------------------------------

@router.get("/iso")
def get_iso():
    return {"iso": state.state.video.iso}


@router.put("/iso")
def set_iso(body: IsoBody):
    state.state.video.iso = body.iso
    return {}


@router.get("/supportedISOs")
def get_supported_isos():
    return {"supportedISOs": SUPPORTED_ISOS}


# ---------------------------------------------------------------------------
# Gain
# ---------------------------------------------------------------------------

@router.get("/gain")
def get_gain():
    return {"gain": state.state.video.gain}


@router.put("/gain")
def set_gain(body: GainBody):
    state.state.video.gain = body.gain
    return {}


@router.get("/supportedGains")
def get_supported_gains():
    return {"supportedGains": SUPPORTED_GAINS}


# ---------------------------------------------------------------------------
# White balance
# ---------------------------------------------------------------------------

@router.get("/whiteBalance")
def get_white_balance():
    return {"whiteBalance": state.state.video.white_balance}


@router.put("/whiteBalance")
def set_white_balance(body: WhiteBalanceBody):
    state.state.video.white_balance = body.whiteBalance
    return {}


@router.get("/whiteBalance/description")
def get_white_balance_description():
    return {"whiteBalance": {"min": 2500, "max": 10000}}


@router.put("/whiteBalance/doAuto")
def do_auto_white_balance():
    state.state.video.white_balance = 5600
    return {}


@router.get("/whiteBalanceTint")
def get_white_balance_tint():
    return {"whiteBalanceTint": state.state.video.white_balance_tint}


@router.put("/whiteBalanceTint")
def set_white_balance_tint(body: WhiteBalanceTintBody):
    state.state.video.white_balance_tint = body.whiteBalanceTint
    return {}


@router.get("/whiteBalanceTint/description")
def get_white_balance_tint_description():
    return {"whiteBalanceTint": {"min": -50, "max": 50}}


# ---------------------------------------------------------------------------
# ND filter
# ---------------------------------------------------------------------------

@router.get("/ndFilter")
def get_nd_filter():
    return {"stop": state.state.video.nd_filter_stop}


@router.put("/ndFilter")
def set_nd_filter(body: NDFilterBody):
    state.state.video.nd_filter_stop = body.stop
    return {}


@router.get("/supportedNDFilters")
def get_supported_nd_filters():
    return {"supportedStops": SUPPORTED_ND_STOPS}


@router.get("/supportedNDFilterDisplayModes")
def get_supported_nd_display_modes():
    return {"supportedDisplayModes": ["Stop", "Number", "Fraction"]}


@router.get("/ndFilter/displayMode")
def get_nd_filter_display_mode():
    return {"displayMode": state.state.video.nd_filter_display_mode}


@router.put("/ndFilter/displayMode")
def set_nd_filter_display_mode(body: NDFilterDisplayModeBody):
    state.state.video.nd_filter_display_mode = body.displayMode
    return {}


@router.get("/ndFilterSelectable")
def get_nd_filter_selectable():
    return {"selectable": state.state.video.nd_filter_supported}


# ---------------------------------------------------------------------------
# Shutter
# ---------------------------------------------------------------------------

@router.get("/shutter")
def get_shutter():
    v = state.state.video
    return {
        "continuousShutterAutoExposure": v.shutter_continuous_auto,
        "shutterSpeed": v.shutter_speed,
        "shutterAngle": v.shutter_angle,
    }


@router.put("/shutter")
def set_shutter(body: ShutterBody):
    v = state.state.video
    if body.continuousShutterAutoExposure is not None:
        v.shutter_continuous_auto = body.continuousShutterAutoExposure
    if body.shutterSpeed is not None:
        v.shutter_speed = body.shutterSpeed
    elif body.shutterAngle is not None:
        v.shutter_angle = body.shutterAngle
    return {}


@router.get("/shutter/measurement")
def get_shutter_measurement():
    return {"measurement": state.state.video.shutter_measurement}


@router.put("/shutter/measurement")
def set_shutter_measurement(body: ShutterMeasurementBody):
    state.state.video.shutter_measurement = body.measurement
    return {}


@router.get("/supportedShutters")
def get_supported_shutters():
    return {
        "shutterAngles": SUPPORTED_SHUTTER_ANGLES,
        "shutterSpeeds": SUPPORTED_SHUTTER_SPEEDS,
    }


@router.get("/flickerFreeShutters")
def get_flicker_free_shutters():
    return {
        "shutterAngles": [144, 172],
        "shutterSpeeds": [50, 100],
    }


# ---------------------------------------------------------------------------
# Auto exposure
# ---------------------------------------------------------------------------

@router.get("/autoExposure")
def get_auto_exposure():
    v = state.state.video
    return {"mode": v.auto_exposure_mode, "type": v.auto_exposure_type}


@router.put("/autoExposure")
def set_auto_exposure(body: AutoExposureBody):
    state.state.video.auto_exposure_mode = body.mode
    if body.type is not None:
        state.state.video.auto_exposure_type = body.type
    return {}


# ---------------------------------------------------------------------------
# Detail sharpening
# ---------------------------------------------------------------------------

@router.get("/detailSharpening")
def get_detail_sharpening():
    return {"enabled": state.state.video.detail_sharpening_enabled}


@router.put("/detailSharpening")
def set_detail_sharpening(body: DetailSharpeningBody):
    state.state.video.detail_sharpening_enabled = body.enabled
    return {}


@router.get("/detailSharpeningLevel")
def get_detail_sharpening_level():
    return {"level": state.state.video.detail_sharpening_level}


@router.put("/detailSharpeningLevel")
def set_detail_sharpening_level(body: DetailSharpeningLevelBody):
    state.state.video.detail_sharpening_level = body.level
    return {}
