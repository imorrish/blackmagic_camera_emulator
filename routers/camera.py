from fastapi import APIRouter
import state
from models import ColorBarsBody, ProgramFeedBody, EnabledBody, PowerDisplayModeBody

router = APIRouter(prefix="/camera", tags=["camera"])


@router.get("/colorBars")
def get_color_bars():
    return {"enabled": state.state.camera.color_bars}


@router.put("/colorBars")
def set_color_bars(body: ColorBarsBody):
    state.state.camera.color_bars = body.enabled
    return {}


@router.get("/programFeedDisplay")
def get_program_feed():
    return {"enabled": state.state.camera.program_feed_display}


@router.put("/programFeedDisplay")
def set_program_feed(body: ProgramFeedBody):
    state.state.camera.program_feed_display = body.enabled
    return {}


@router.get("/tallyStatus")
def get_tally():
    return {"status": state.state.camera.tally_status}


@router.get("/power")
def get_power():
    c = state.state.camera
    return {
        "source": c.power_source,
        "milliVolt": c.power_milli_volt,
        "batteries": c.batteries,
    }


@router.get("/power/displayMode")
def get_power_display_mode():
    return {"mode": state.state.camera.power_display_mode}


@router.put("/power/displayMode")
def set_power_display_mode(body: PowerDisplayModeBody):
    state.state.camera.power_display_mode = body.mode
    return {}


@router.get("/timingReferenceLock")
def get_timing_reference_lock():
    return {"locked": state.state.camera.timing_reference_locked}
