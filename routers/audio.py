from fastapi import APIRouter, HTTPException
import state
from models import AudioLevelBody, AudioInputBody, PhantomPowerBody, PaddingBody, LowCutFilterBody
from state import AudioChannelState

router = APIRouter(prefix="/audio", tags=["audio"])

SUPPORTED_INPUTS = ["None", "XLR", "BalancedXLR", "Camera", "3.5mm", "RCA", "HDMI"]


def _get_channel(idx: int) -> AudioChannelState:
    ch = state.state.audio.channels.get(idx)
    if ch is None:
        raise HTTPException(status_code=404, detail=f"Channel {idx} not found")
    return ch


@router.get("/channels")
def get_channels():
    return {"numberOfChannels": len(state.state.audio.channels)}


@router.get("/supportedInputs")
def get_supported_inputs():
    return {"supportedInputs": SUPPORTED_INPUTS}


# ---------------------------------------------------------------------------
# Per-channel endpoints
# ---------------------------------------------------------------------------

@router.get("/channel/{idx}/input")
def get_input(idx: int):
    return {"input": _get_channel(idx).input}


@router.put("/channel/{idx}/input")
def set_input(idx: int, body: AudioInputBody):
    _get_channel(idx).input = body.input
    return {}


@router.get("/channel/{idx}/input/description")
def get_input_description(idx: int):
    _get_channel(idx)  # validate
    return {
        "gain": {"min": -128.0, "max": 36.0},
        "capabilities": {
            "phantom": True,
            "lowCut": True,
            "padding": True,
        },
    }


@router.get("/channel/{idx}/supportedInputs")
def get_channel_supported_inputs(idx: int):
    _get_channel(idx)
    return {"supportedInputs": SUPPORTED_INPUTS}


@router.get("/channel/{idx}/level")
def get_level(idx: int):
    ch = _get_channel(idx)
    return {"gain": ch.gain, "normalised": ch.normalised}


@router.put("/channel/{idx}/level")
def set_level(idx: int, body: AudioLevelBody):
    ch = _get_channel(idx)
    if body.gain is not None:
        ch.gain = body.gain
    if body.normalised is not None:
        ch.normalised = body.normalised
    return {}


@router.get("/channel/{idx}/phantomPower")
def get_phantom_power(idx: int):
    return {"enabled": _get_channel(idx).phantom_power}


@router.put("/channel/{idx}/phantomPower")
def set_phantom_power(idx: int, body: PhantomPowerBody):
    _get_channel(idx).phantom_power = body.enabled
    return {}


@router.get("/channel/{idx}/padding")
def get_padding(idx: int):
    return {"enabled": _get_channel(idx).padding}


@router.put("/channel/{idx}/padding")
def set_padding(idx: int, body: PaddingBody):
    _get_channel(idx).padding = body.enabled
    return {}


@router.get("/channel/{idx}/lowCutFilter")
def get_low_cut(idx: int):
    return {"enabled": _get_channel(idx).low_cut_filter}


@router.put("/channel/{idx}/lowCutFilter")
def set_low_cut(idx: int, body: LowCutFilterBody):
    _get_channel(idx).low_cut_filter = body.enabled
    return {}


@router.get("/channel/{idx}/available")
def get_available(idx: int):
    return {"available": _get_channel(idx).available}
