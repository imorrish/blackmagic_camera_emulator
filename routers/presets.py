from fastapi import APIRouter, HTTPException
import state
from models import ActivePresetBody

router = APIRouter(prefix="/presets", tags=["presets"])


@router.get("")
def get_presets():
    return {"presets": state.state.presets.presets}


@router.get("/active")
def get_active_preset():
    return {"preset": state.state.presets.active}


@router.put("/active")
def set_active_preset(body: ActivePresetBody):
    if body.preset not in state.state.presets.presets:
        raise HTTPException(status_code=404, detail=f"Preset '{body.preset}' not found")
    state.state.presets.active = body.preset
    return {}


@router.put("/{preset_name}")
def save_preset(preset_name: str):
    """Save current camera state as a named preset (name only — no binary content)."""
    if preset_name not in state.state.presets.presets:
        state.state.presets.presets.append(preset_name)
    state.state.presets.active = preset_name
    return {}


@router.delete("/{preset_name}")
def delete_preset(preset_name: str):
    if preset_name not in state.state.presets.presets:
        raise HTTPException(status_code=404, detail=f"Preset '{preset_name}' not found")
    state.state.presets.presets.remove(preset_name)
    if state.state.presets.active == preset_name:
        state.state.presets.active = state.state.presets.presets[0] if state.state.presets.presets else ""
    return {}
