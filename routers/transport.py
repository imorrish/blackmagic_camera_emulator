from fastapi import APIRouter
import state
from models import TransportModeBody, RecordBody, PlaybackBody

router = APIRouter(prefix="/transports/0", tags=["transport"])


@router.get("")
def get_transport():
    return {"mode": state.state.transport.mode}


@router.put("")
def set_transport(body: TransportModeBody):
    state.state.transport.mode = body.mode
    return {}


# ---------------------------------------------------------------------------
# Stop
# ---------------------------------------------------------------------------

@router.get("/stop")
def get_stop():
    return {"playing": False, "recording": state.state.transport.recording}


@router.put("/stop")
@router.post("/stop")
def do_stop():
    state.state.transport.playing = False
    state.state.transport.recording = False
    return {}


# ---------------------------------------------------------------------------
# Play
# ---------------------------------------------------------------------------

@router.get("/play")
def get_play():
    return {"playing": state.state.transport.playing}


@router.put("/play")
@router.post("/play")
def do_play():
    state.state.transport.playing = True
    state.state.transport.recording = False
    return {}


# ---------------------------------------------------------------------------
# Playback
# ---------------------------------------------------------------------------

@router.get("/playback")
def get_playback():
    t = state.state.transport
    return {
        "type": t.playback_type,
        "loop": t.playback_loop,
        "singleClip": t.playback_single_clip,
        "speed": t.playback_speed,
        "position": t.playback_position,
    }


@router.put("/playback")
def set_playback(body: PlaybackBody):
    t = state.state.transport
    if body.type is not None:
        t.playback_type = body.type
    if body.loop is not None:
        t.playback_loop = body.loop
    if body.singleClip is not None:
        t.playback_single_clip = body.singleClip
    if body.speed is not None:
        t.playback_speed = body.speed
    if body.position is not None:
        t.playback_position = body.position
    return {}


# ---------------------------------------------------------------------------
# Record
# ---------------------------------------------------------------------------

@router.get("/record")
def get_record():
    return {"recording": state.state.transport.recording}


@router.put("/record")
def set_record(body: RecordBody):
    state.state.transport.recording = True
    state.state.transport.playing = False
    if body.clipName:
        state.state.transport.clip_name = body.clipName
    return {}


@router.post("/record")
def start_record(body: RecordBody = RecordBody()):
    state.state.transport.recording = True
    state.state.transport.playing = False
    if body.clipName:
        state.state.transport.clip_name = body.clipName
    return {}


# ---------------------------------------------------------------------------
# Clip index
# ---------------------------------------------------------------------------

@router.get("/clipIndex")
def get_clip_index():
    return {"clipIndex": state.state.transport.clip_index}


# ---------------------------------------------------------------------------
# Timecode
# ---------------------------------------------------------------------------

@router.get("/timecode")
def get_timecode():
    t = state.state.transport
    return {"display": t.timecode_display, "timeline": t.timecode_timeline}


@router.get("/timecode/source")
def get_timecode_source():
    return {"timecode": state.state.transport.timecode_source}
