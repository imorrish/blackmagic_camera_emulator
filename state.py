"""In-memory camera state. All routers import and mutate this module-level object."""

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Sub-state dataclasses
# ---------------------------------------------------------------------------

@dataclass
class LensState:
    focus_normalised: float = 0.5
    iris_normalised: float = 0.5
    iris_aperture_stop: float = 4.0
    iris_aperture_number: float = 4.0
    iris_continuous_auto: bool = False
    zoom_normalised: float = 0.0
    zoom_focal_length: int = 24
    ois_enabled: bool = False
    focus_controllable: bool = True
    iris_controllable: bool = True
    zoom_controllable: bool = True


@dataclass
class VideoState:
    iso: int = 400
    gain: int = 0
    white_balance: int = 5600
    white_balance_tint: int = 0
    shutter_speed: int = 50        # 1/N seconds stored as N
    shutter_angle: int = 180
    shutter_measurement: str = "ShutterAngle"  # ShutterAngle | ShutterSpeed
    shutter_continuous_auto: bool = False
    auto_exposure_mode: str = "Off"  # Off | Continuous | OneShot
    auto_exposure_type: str = "Iris"
    nd_filter_stop: float = 0.0
    nd_filter_display_mode: str = "Stop"  # Stop | Number | Fraction
    nd_filter_supported: bool = True
    detail_sharpening_enabled: bool = False
    detail_sharpening_level: str = "Medium"  # Low | Medium | High


@dataclass
class TransportState:
    mode: str = "InputPreview"          # InputPreview | Output
    recording: bool = False
    playing: bool = False
    playback_type: str = "Play"         # Play | Jog | Shuttle | Var
    playback_loop: bool = False
    playback_single_clip: bool = False
    playback_speed: float = 1.0
    playback_position: int = 0
    clip_name: Optional[str] = None
    clip_index: Optional[int] = None
    timecode_display: str = "00:00:00:00"
    timecode_timeline: str = "00:00:00:00"
    timecode_source: str = "Timeline"   # Timeline | Clip


@dataclass
class AudioChannelState:
    input: str = "None"                 # None | XLR | BalancedXLR | Camera | 3.5mm | ...
    gain: float = 0.0
    normalised: float = 0.5
    phantom_power: bool = False
    padding: bool = False
    low_cut_filter: bool = False
    available: bool = True


@dataclass
class AudioState:
    channels: dict = field(default_factory=lambda: {
        0: AudioChannelState(input="XLR", gain=0.0, normalised=0.5),
        1: AudioChannelState(input="XLR", gain=0.0, normalised=0.5),
    })


@dataclass
class ColorWheelState:
    red: float = 0.0
    green: float = 0.0
    blue: float = 0.0
    luma: float = 0.0


@dataclass
class ColorCorrectionState:
    lift: ColorWheelState = field(default_factory=ColorWheelState)
    gamma: ColorWheelState = field(default_factory=ColorWheelState)
    gain: ColorWheelState = field(default_factory=lambda: ColorWheelState(red=1.0, green=1.0, blue=1.0, luma=1.0))
    offset: ColorWheelState = field(default_factory=ColorWheelState)
    contrast_pivot: float = 0.5
    contrast_adjust: float = 1.0
    hue: float = 0.0
    saturation: float = 1.0
    luma_contribution: float = 1.0


@dataclass
class MonitoringDisplayState:
    clean_feed: bool = False
    display_lut: bool = False
    zebra: bool = False
    focus_assist_mode: str = "Peak"          # Peak | ColoredLines
    focus_assist_color: str = "Green"        # Red | Green | Blue | White | Black
    focus_assist_intensity: int = 50
    frame_guide: bool = False
    frame_grids: bool = False
    safe_area: bool = False
    false_color: bool = False


@dataclass
class MonitoringState:
    displays: list = field(default_factory=lambda: ["main"])
    display_state: dict = field(default_factory=lambda: {
        "main": MonitoringDisplayState(),
    })
    frame_guide_ratio: str = "2.39:1"
    frame_guide_ratio_presets: list = field(default_factory=lambda: [
        "2.39:1", "2.35:1", "1.85:1", "16:9", "14:9", "4:3",
    ])
    safe_area_percent: int = 80
    frame_grids: list = field(default_factory=lambda: [])  # Thirds | Crosshair | Dot | Horizon
    focus_assist_mode: str = "Peak"
    focus_assist_color: str = "Green"
    focus_assist_intensity: int = 50


@dataclass
class PowerBattery:
    milli_volt: int = 12600
    charge_remaining_percent: int = 85
    status_flags: list = field(default_factory=list)


@dataclass
class CameraSystemState:
    color_bars: bool = False
    program_feed_display: bool = False
    tally_status: str = "None"          # None | Preview | Program
    power_source: str = "Battery"       # Battery | AC | Fiber | USB | POE
    power_milli_volt: int = 12600
    batteries: list = field(default_factory=lambda: [
        PowerBattery().__dict__,
    ])
    power_display_mode: str = "Percentage"  # Percentage | Voltage
    timing_reference_locked: bool = False
    codec: str = "ProRes:HQ"
    container: str = "MOV"
    video_format_name: str = "1920x1080p25"
    video_frame_rate: str = "25"
    video_height: int = 1080
    video_width: int = 1920
    video_interlaced: bool = False
    format_frame_rate: str = "25"
    off_speed_enabled: bool = False
    off_speed_frame_rate: str = "25"
    record_resolution_width: int = 1920
    record_resolution_height: int = 1080
    sensor_resolution_width: int = 1920
    sensor_resolution_height: int = 1080
    product_name: str = "Blackmagic Camera Emulator"
    device_name: str = "Blackmagic"
    software_version: str = "7.9.1"


@dataclass
class SlateClipData:
    clip_name: str = ""
    reel: str = "A001"
    scene: str = "1"
    scene_location: str = ""
    scene_time: str = ""
    shot_type: str = "WS"
    take: int = 1
    take_type: str = "NG"
    good_take: bool = False


@dataclass
class SlateLensData:
    lens_type: str = ""
    iris: str = ""
    focal_length: str = ""
    distance: str = ""
    filter: str = ""


@dataclass
class SlateProjectData:
    project_name: str = "My Project"
    director: str = ""
    camera: str = "A"
    camera_operator: str = ""


@dataclass
class SlateState:
    clip: SlateClipData = field(default_factory=SlateClipData)
    lens: SlateLensData = field(default_factory=SlateLensData)
    project: SlateProjectData = field(default_factory=SlateProjectData)


@dataclass
class MediaDevice:
    volume: str = "SSD1"
    device_name: str = "SSD1"
    remaining_record_time: str = "02:30:00"
    total_space: int = 500_000_000_000      # 500 GB in bytes
    remaining_space: int = 400_000_000_000
    clip_count: int = 12
    state: str = "Mounted"                  # None | Scanning | Mounted | Uninitialised | Formatting | RaidComponent


@dataclass
class MediaState:
    working_set: list = field(default_factory=lambda: [
        MediaDevice().__dict__,
    ])
    active_index: int = 0
    active_device_name: str = "SSD1"


@dataclass
class PresetsState:
    presets: list = field(default_factory=lambda: ["Default"])
    active: str = "Default"


# ---------------------------------------------------------------------------
# Root camera state
# ---------------------------------------------------------------------------

@dataclass
class CameraState:
    lens: LensState = field(default_factory=LensState)
    video: VideoState = field(default_factory=VideoState)
    transport: TransportState = field(default_factory=TransportState)
    audio: AudioState = field(default_factory=AudioState)
    color: ColorCorrectionState = field(default_factory=ColorCorrectionState)
    monitoring: MonitoringState = field(default_factory=MonitoringState)
    camera: CameraSystemState = field(default_factory=CameraSystemState)
    slate: SlateState = field(default_factory=SlateState)
    media: MediaState = field(default_factory=MediaState)
    presets: PresetsState = field(default_factory=PresetsState)


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

_DEFAULTS: CameraState = CameraState()
state: CameraState = CameraState()


def reset() -> None:
    """Restore all state to defaults."""
    global state
    state = deepcopy(_DEFAULTS)
