from fastapi import APIRouter, HTTPException
import state
from models import ActiveMediaBody

router = APIRouter(prefix="/media", tags=["media"])


@router.get("/workingset")
def get_working_set():
    ws = state.state.media
    return {
        "size": len(ws.working_set),
        "workingset": [
            {
                "volume": d["volume"],
                "deviceName": d["device_name"],
                "remainingRecordTime": d["remaining_record_time"],
                "totalSpace": d["total_space"],
                "remainingSpace": d["remaining_space"],
                "clipCount": d["clip_count"],
            }
            for d in ws.working_set
        ],
    }


@router.get("/active")
def get_active():
    ws = state.state.media
    return {"workingsetIndex": ws.active_index, "deviceName": ws.active_device_name}


@router.put("/active")
def set_active(body: ActiveMediaBody):
    ws = state.state.media
    if body.workingsetIndex is not None:
        if body.workingsetIndex >= len(ws.working_set):
            raise HTTPException(status_code=404, detail="Working set index out of range")
        ws.active_index = body.workingsetIndex
        ws.active_device_name = ws.working_set[body.workingsetIndex]["device_name"]
    elif body.deviceName is not None:
        for i, d in enumerate(ws.working_set):
            if d["device_name"] == body.deviceName:
                ws.active_index = i
                ws.active_device_name = body.deviceName
                return {}
        raise HTTPException(status_code=404, detail=f"Device '{body.deviceName}' not found")
    return {}


@router.get("/devices/doformatSupportedFilesystems")
def get_format_filesystems():
    return ["exFAT", "HFS+"]


@router.get("/devices/{device_name}")
def get_device(device_name: str):
    for d in state.state.media.working_set:
        if d["device_name"] == device_name:
            return {"state": d["state"]}
    raise HTTPException(status_code=404, detail=f"Device '{device_name}' not found")
