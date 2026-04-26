"""Pydantic request/response models matching the Blackmagic camera REST API spec."""

from typing import Optional
from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Lens
# ---------------------------------------------------------------------------

class IrisBody(BaseModel):
    continuousApertureAutoExposure: Optional[bool] = None
    apertureStop: Optional[float] = None
    normalised: Optional[float] = None
    apertureNumber: Optional[float] = None


class ZoomBody(BaseModel):
    focalLength: Optional[int] = None
    normalised: Optional[float] = None


class FocusBody(BaseModel):
    normalised: Optional[float] = None


class AutoFocusBody(BaseModel):
    position: Optional[dict] = None


class LensDescription(BaseModel):
    controllable: bool
    apertureStop: Optional[dict] = None
    focalLength: Optional[dict] = None
    focusDistance: Optional[dict] = None


# ---------------------------------------------------------------------------
# Video
# ---------------------------------------------------------------------------

class IsoBody(BaseModel):
    iso: int


class GainBody(BaseModel):
    gain: int


class WhiteBalanceBody(BaseModel):
    whiteBalance: int


class WhiteBalanceTintBody(BaseModel):
    whiteBalanceTint: int


class NDFilterBody(BaseModel):
    stop: float


class NDFilterDisplayModeBody(BaseModel):
    displayMode: str  # Stop | Number | Fraction


class ShutterBody(BaseModel):
    continuousShutterAutoExposure: Optional[bool] = None
    shutterSpeed: Optional[int] = None
    shutterAngle: Optional[int] = None


class ShutterMeasurementBody(BaseModel):
    measurement: str  # ShutterAngle | ShutterSpeed


class AutoExposureBody(BaseModel):
    mode: str  # Off | Continuous | OneShot
    type: Optional[str] = None


class DetailSharpeningBody(BaseModel):
    enabled: bool


class DetailSharpeningLevelBody(BaseModel):
    level: str  # Low | Medium | High


# ---------------------------------------------------------------------------
# Transport
# ---------------------------------------------------------------------------

class TransportModeBody(BaseModel):
    mode: str  # InputPreview | Output


class RecordBody(BaseModel):
    clipName: Optional[str] = None


class PlaybackBody(BaseModel):
    type: Optional[str] = None     # Play | Jog | Shuttle | Var
    loop: Optional[bool] = None
    singleClip: Optional[bool] = None
    speed: Optional[float] = None
    position: Optional[int] = None


# ---------------------------------------------------------------------------
# Audio
# ---------------------------------------------------------------------------

class AudioLevelBody(BaseModel):
    gain: Optional[float] = None
    normalised: Optional[float] = None


class AudioInputBody(BaseModel):
    input: str


class PhantomPowerBody(BaseModel):
    enabled: bool


class PaddingBody(BaseModel):
    enabled: bool


class LowCutFilterBody(BaseModel):
    enabled: bool


# ---------------------------------------------------------------------------
# Color correction
# ---------------------------------------------------------------------------

class ColorWheelBody(BaseModel):
    red: Optional[float] = None
    green: Optional[float] = None
    blue: Optional[float] = None
    luma: Optional[float] = None


class ContrastBody(BaseModel):
    pivot: Optional[float] = None
    adjust: Optional[float] = None


class ColorBody(BaseModel):
    hue: Optional[float] = None
    saturation: Optional[float] = None


class LumaContributionBody(BaseModel):
    lumaContribution: float


# ---------------------------------------------------------------------------
# Monitoring
# ---------------------------------------------------------------------------

class EnabledBody(BaseModel):
    enabled: bool


class FocusAssistBody(BaseModel):
    mode: Optional[str] = None        # Peak | ColoredLines
    color: Optional[str] = None       # Red | Green | Blue | White | Black
    intensity: Optional[int] = None


class FrameGuideRatioBody(BaseModel):
    ratio: str


class FrameGridsBody(BaseModel):
    frameGrids: list


class SafeAreaPercentBody(BaseModel):
    percent: int


# ---------------------------------------------------------------------------
# System
# ---------------------------------------------------------------------------

class CodecFormatBody(BaseModel):
    codec: str
    container: str


class VideoFormatBody(BaseModel):
    name: Optional[str] = None
    frameRate: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None
    interlaced: Optional[bool] = None


class SystemFormatBody(BaseModel):
    codec: Optional[str] = None
    frameRate: Optional[str] = None
    maxOffSpeedFrameRate: Optional[int] = None
    minOffSpeedFrameRate: Optional[int] = None
    offSpeedEnabled: Optional[bool] = None
    offSpeedFrameRate: Optional[str] = None
    recordResolution: Optional[dict] = None
    sensorResolution: Optional[dict] = None


# ---------------------------------------------------------------------------
# Camera
# ---------------------------------------------------------------------------

class ColorBarsBody(BaseModel):
    enabled: bool


class ProgramFeedBody(BaseModel):
    enabled: bool


class PowerDisplayModeBody(BaseModel):
    mode: str  # Percentage | Voltage


# ---------------------------------------------------------------------------
# Presets
# ---------------------------------------------------------------------------

class ActivePresetBody(BaseModel):
    preset: str


# ---------------------------------------------------------------------------
# Media
# ---------------------------------------------------------------------------

class ActiveMediaBody(BaseModel):
    workingsetIndex: Optional[int] = None
    deviceName: Optional[str] = None


# ---------------------------------------------------------------------------
# Slate  (nested structure mirroring the spec)
# ---------------------------------------------------------------------------

class SlateClipBody(BaseModel):
    clipName: Optional[str] = None
    reel: Optional[str] = None
    scene: Optional[str] = None
    sceneLocation: Optional[str] = None
    sceneTime: Optional[str] = None
    shotType: Optional[str] = None
    take: Optional[int] = None
    takeType: Optional[str] = None
    goodTake: Optional[bool] = None


class SlateLensBody(BaseModel):
    lensType: Optional[str] = None
    iris: Optional[str] = None
    focalLength: Optional[str] = None
    distance: Optional[str] = None
    filter: Optional[str] = None


class SlateProjectBody(BaseModel):
    projectName: Optional[str] = None
    director: Optional[str] = None
    camera: Optional[str] = None
    cameraOperator: Optional[str] = None


class SlateBody(BaseModel):
    clip: Optional[SlateClipBody] = None
    lens: Optional[SlateLensBody] = None
    project: Optional[SlateProjectBody] = None
