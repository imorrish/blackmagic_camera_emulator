from fastapi import APIRouter
import state
from models import IrisBody, ZoomBody, FocusBody, AutoFocusBody

router = APIRouter(prefix="/lens", tags=["lens"])


# ---------------------------------------------------------------------------
# Iris
# ---------------------------------------------------------------------------

@router.get("/iris")
def get_iris():
    s = state.state.lens
    return {
        "continuousApertureAutoExposure": s.iris_continuous_auto,
        "apertureStop": s.iris_aperture_stop,
        "normalised": s.iris_normalised,
        "apertureNumber": s.iris_aperture_number,
    }


@router.put("/iris")
def set_iris(body: IrisBody):
    s = state.state.lens
    if body.continuousApertureAutoExposure is not None:
        s.iris_continuous_auto = body.continuousApertureAutoExposure
    if body.apertureStop is not None:
        s.iris_aperture_stop = body.apertureStop
        s.iris_normalised = max(0.0, min(1.0, (body.apertureStop - 1.0) / 15.0))
        s.iris_aperture_number = body.apertureStop
    elif body.normalised is not None:
        s.iris_normalised = body.normalised
        s.iris_aperture_stop = 1.0 + body.normalised * 15.0
        s.iris_aperture_number = s.iris_aperture_stop
    elif body.apertureNumber is not None:
        s.iris_aperture_number = body.apertureNumber
        s.iris_aperture_stop = body.apertureNumber
        s.iris_normalised = max(0.0, min(1.0, (body.apertureNumber - 1.0) / 15.0))
    return {}


@router.get("/iris/description")
def get_iris_description():
    return {
        "controllable": state.state.lens.iris_controllable,
        "apertureStop": {"min": 1.0, "max": 16.0},
    }


# ---------------------------------------------------------------------------
# Zoom
# ---------------------------------------------------------------------------

@router.get("/zoom")
def get_zoom():
    s = state.state.lens
    return {"focalLength": s.zoom_focal_length, "normalised": s.zoom_normalised}


@router.put("/zoom")
def set_zoom(body: ZoomBody):
    s = state.state.lens
    if body.focalLength is not None:
        s.zoom_focal_length = body.focalLength
        s.zoom_normalised = max(0.0, min(1.0, (body.focalLength - 14) / (200 - 14)))
    elif body.normalised is not None:
        s.zoom_normalised = body.normalised
        s.zoom_focal_length = int(14 + body.normalised * (200 - 14))
    return {}


@router.get("/zoom/description")
def get_zoom_description():
    return {
        "controllable": state.state.lens.zoom_controllable,
        "focalLength": {"adjustable": True, "min": 14, "max": 200},
    }


# ---------------------------------------------------------------------------
# Focus
# ---------------------------------------------------------------------------

@router.get("/focus")
def get_focus():
    return {"normalised": state.state.lens.focus_normalised}


@router.put("/focus")
def set_focus(body: FocusBody):
    if body.normalised is not None:
        state.state.lens.focus_normalised = body.normalised
    return {}


@router.put("/focus/doAutoFocus")
def do_auto_focus(body: AutoFocusBody = AutoFocusBody()):
    # Simulate auto-focus by moving to centre
    state.state.lens.focus_normalised = 0.5
    return {}


@router.get("/focus/description")
def get_focus_description():
    return {
        "controllable": state.state.lens.focus_controllable,
        "focusDistance": {"adjustable": True, "min": 0.0, "max": 1.0},
    }
