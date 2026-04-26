from fastapi import APIRouter, HTTPException
import state
from models import (
    EnabledBody, FocusAssistBody, FrameGuideRatioBody,
    FrameGridsBody, SafeAreaPercentBody,
)
from state import MonitoringDisplayState

router = APIRouter(prefix="/monitoring", tags=["monitoring"])


def _get_display(name: str) -> MonitoringDisplayState:
    d = state.state.monitoring.display_state.get(name)
    if d is None:
        raise HTTPException(status_code=404, detail=f"Display '{name}' not found")
    return d


@router.get("/display")
def get_displays():
    return {"displays": state.state.monitoring.displays}


# ---------------------------------------------------------------------------
# Per-display endpoints
# ---------------------------------------------------------------------------

@router.get("/{display}/cleanFeed")
def get_clean_feed(display: str):
    return {"enabled": _get_display(display).clean_feed}


@router.put("/{display}/cleanFeed")
def set_clean_feed(display: str, body: EnabledBody):
    _get_display(display).clean_feed = body.enabled
    return {}


@router.get("/{display}/displayLUT")
def get_display_lut(display: str):
    return {"enabled": _get_display(display).display_lut}


@router.put("/{display}/displayLUT")
def set_display_lut(display: str, body: EnabledBody):
    _get_display(display).display_lut = body.enabled
    return {}


@router.get("/{display}/zebra")
def get_zebra(display: str):
    return {"enabled": _get_display(display).zebra}


@router.put("/{display}/zebra")
def set_zebra(display: str, body: EnabledBody):
    _get_display(display).zebra = body.enabled
    return {}


@router.get("/{display}/focusAssist")
def get_display_focus_assist(display: str):
    d = _get_display(display)
    return {
        "mode": d.focus_assist_mode,
        "color": d.focus_assist_color,
        "intensity": d.focus_assist_intensity,
    }


@router.put("/{display}/focusAssist")
def set_display_focus_assist(display: str, body: FocusAssistBody):
    d = _get_display(display)
    if body.mode is not None:
        d.focus_assist_mode = body.mode
    if body.color is not None:
        d.focus_assist_color = body.color
    if body.intensity is not None:
        d.focus_assist_intensity = body.intensity
    return {}


@router.get("/{display}/frameGuide")
def get_frame_guide(display: str):
    return {"enabled": _get_display(display).frame_guide}


@router.put("/{display}/frameGuide")
def set_frame_guide(display: str, body: EnabledBody):
    _get_display(display).frame_guide = body.enabled
    return {}


@router.get("/{display}/frameGrids")
def get_display_frame_grids(display: str):
    return {"enabled": _get_display(display).frame_grids}


@router.put("/{display}/frameGrids")
def set_display_frame_grids(display: str, body: EnabledBody):
    _get_display(display).frame_grids = body.enabled
    return {}


@router.get("/{display}/safeArea")
def get_safe_area(display: str):
    return {"enabled": _get_display(display).safe_area}


@router.put("/{display}/safeArea")
def set_safe_area(display: str, body: EnabledBody):
    _get_display(display).safe_area = body.enabled
    return {}


@router.get("/{display}/falseColor")
def get_false_color(display: str):
    return {"enabled": _get_display(display).false_color}


@router.put("/{display}/falseColor")
def set_false_color(display: str, body: EnabledBody):
    _get_display(display).false_color = body.enabled
    return {}


# ---------------------------------------------------------------------------
# Global monitoring settings
# NOTE: These must be registered BEFORE the /{display}/* routes so they are
# not swallowed by the display path parameter.  They are registered via a
# separate prefix-less include in main.py so order here does not matter, but
# we group them logically.
# ---------------------------------------------------------------------------

@router.get("/focusAssist")
def get_global_focus_assist():
    m = state.state.monitoring
    return {
        "mode": m.focus_assist_mode,
        "color": m.focus_assist_color,
        "intensity": m.focus_assist_intensity,
    }


@router.put("/focusAssist")
def set_global_focus_assist(body: FocusAssistBody):
    m = state.state.monitoring
    if body.mode is not None:
        m.focus_assist_mode = body.mode
    if body.color is not None:
        m.focus_assist_color = body.color
    if body.intensity is not None:
        m.focus_assist_intensity = body.intensity
    return {}


@router.get("/frameGuideRatio")
def get_frame_guide_ratio():
    return {"ratio": state.state.monitoring.frame_guide_ratio}


@router.put("/frameGuideRatio")
def set_frame_guide_ratio(body: FrameGuideRatioBody):
    state.state.monitoring.frame_guide_ratio = body.ratio
    return {}


@router.get("/frameGuideRatio/presets")
def get_frame_guide_ratio_presets():
    return {"presets": state.state.monitoring.frame_guide_ratio_presets}


@router.get("/frameGrids")
def get_global_frame_grids():
    return {"frameGrids": state.state.monitoring.frame_grids}


@router.put("/frameGrids")
def set_global_frame_grids(body: FrameGridsBody):
    state.state.monitoring.frame_grids = body.frameGrids
    return {}


@router.get("/safeAreaPercent")
def get_safe_area_percent():
    return {"percent": state.state.monitoring.safe_area_percent}


@router.put("/safeAreaPercent")
def set_safe_area_percent(body: SafeAreaPercentBody):
    state.state.monitoring.safe_area_percent = body.percent
    return {}
