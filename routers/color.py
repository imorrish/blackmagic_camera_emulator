from fastapi import APIRouter
import state
from models import (
    ColorWheelBody, ContrastBody, ColorBody, LumaContributionBody,
)

router = APIRouter(prefix="/colorCorrection", tags=["color"])


def _wheel_response(w) -> dict:
    return {"red": w.red, "green": w.green, "blue": w.blue, "luma": w.luma}


def _apply_wheel(wheel, body: ColorWheelBody):
    if body.red is not None:
        wheel.red = body.red
    if body.green is not None:
        wheel.green = body.green
    if body.blue is not None:
        wheel.blue = body.blue
    if body.luma is not None:
        wheel.luma = body.luma


@router.get("/lift")
def get_lift():
    return _wheel_response(state.state.color.lift)


@router.put("/lift")
def set_lift(body: ColorWheelBody):
    _apply_wheel(state.state.color.lift, body)
    return {}


@router.get("/gamma")
def get_gamma():
    return _wheel_response(state.state.color.gamma)


@router.put("/gamma")
def set_gamma(body: ColorWheelBody):
    _apply_wheel(state.state.color.gamma, body)
    return {}


@router.get("/gain")
def get_gain():
    return _wheel_response(state.state.color.gain)


@router.put("/gain")
def set_gain(body: ColorWheelBody):
    _apply_wheel(state.state.color.gain, body)
    return {}


@router.get("/offset")
def get_offset():
    return _wheel_response(state.state.color.offset)


@router.put("/offset")
def set_offset(body: ColorWheelBody):
    _apply_wheel(state.state.color.offset, body)
    return {}


@router.get("/contrast")
def get_contrast():
    c = state.state.color
    return {"pivot": c.contrast_pivot, "adjust": c.contrast_adjust}


@router.put("/contrast")
def set_contrast(body: ContrastBody):
    c = state.state.color
    if body.pivot is not None:
        c.contrast_pivot = body.pivot
    if body.adjust is not None:
        c.contrast_adjust = body.adjust
    return {}


@router.get("/color")
def get_color():
    c = state.state.color
    return {"hue": c.hue, "saturation": c.saturation}


@router.put("/color")
def set_color(body: ColorBody):
    c = state.state.color
    if body.hue is not None:
        c.hue = body.hue
    if body.saturation is not None:
        c.saturation = body.saturation
    return {}


@router.get("/lumaContribution")
def get_luma_contribution():
    return {"lumaContribution": state.state.color.luma_contribution}


@router.put("/lumaContribution")
def set_luma_contribution(body: LumaContributionBody):
    state.state.color.luma_contribution = body.lumaContribution
    return {}
