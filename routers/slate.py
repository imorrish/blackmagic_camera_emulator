from fastapi import APIRouter
import state
from models import SlateBody

router = APIRouter(prefix="/slates", tags=["slate"])


def _slate_to_dict() -> dict:
    s = state.state.slate
    return {
        "clip": {
            "clipName": s.clip.clip_name,
            "reel": s.clip.reel,
            "scene": s.clip.scene,
            "sceneLocation": s.clip.scene_location,
            "sceneTime": s.clip.scene_time,
            "shotType": s.clip.shot_type,
            "take": s.clip.take,
            "takeType": s.clip.take_type,
            "goodTake": s.clip.good_take,
        },
        "lens": {
            "lensType": s.lens.lens_type,
            "iris": s.lens.iris,
            "focalLength": s.lens.focal_length,
            "distance": s.lens.distance,
            "filter": s.lens.filter,
        },
        "project": {
            "projectName": s.project.project_name,
            "director": s.project.director,
            "camera": s.project.camera,
            "cameraOperator": s.project.camera_operator,
        },
    }


@router.get("/nextClip")
def get_next_clip():
    return _slate_to_dict()


@router.put("/nextClip")
def set_next_clip(body: SlateBody):
    s = state.state.slate
    if body.clip:
        c = body.clip
        if c.clipName is not None:
            s.clip.clip_name = c.clipName
        if c.reel is not None:
            s.clip.reel = c.reel
        if c.scene is not None:
            s.clip.scene = c.scene
        if c.sceneLocation is not None:
            s.clip.scene_location = c.sceneLocation
        if c.sceneTime is not None:
            s.clip.scene_time = c.sceneTime
        if c.shotType is not None:
            s.clip.shot_type = c.shotType
        if c.take is not None:
            s.clip.take = c.take
        if c.takeType is not None:
            s.clip.take_type = c.takeType
        if c.goodTake is not None:
            s.clip.good_take = c.goodTake
    if body.lens:
        ln = body.lens
        if ln.lensType is not None:
            s.lens.lens_type = ln.lensType
        if ln.iris is not None:
            s.lens.iris = ln.iris
        if ln.focalLength is not None:
            s.lens.focal_length = ln.focalLength
        if ln.distance is not None:
            s.lens.distance = ln.distance
        if ln.filter is not None:
            s.lens.filter = ln.filter
    if body.project:
        p = body.project
        if p.projectName is not None:
            s.project.project_name = p.projectName
        if p.director is not None:
            s.project.director = p.director
        if p.camera is not None:
            s.project.camera = p.camera
        if p.cameraOperator is not None:
            s.project.camera_operator = p.cameraOperator
    return {}


@router.post("/nextClip/resetProjectData")
def reset_project_data():
    s = state.state.slate
    s.project.project_name = ""
    s.project.director = ""
    s.project.camera = "A"
    s.project.camera_operator = ""
    return {}


@router.post("/nextClip/resetLensData")
def reset_lens_data():
    s = state.state.slate
    s.lens.lens_type = ""
    s.lens.iris = ""
    s.lens.focal_length = ""
    s.lens.distance = ""
    s.lens.filter = ""
    return {}
