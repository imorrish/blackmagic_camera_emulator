"""Blackmagic Camera Emulator — FastAPI application.

Run with:
    uvicorn main:app --port 8080 --reload

Connect the Flutter app to: http://127.0.0.1:8080
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import state
from routers import audio, camera, color, lens, media, monitoring, presets, slate, system, transport, video

API_PREFIX = "/control/api/v1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("=" * 60)
    print("Blackmagic Camera Emulator started")
    print(f"  API base : http://127.0.0.1:8080{API_PREFIX}")
    print(f"  Docs     : http://127.0.0.1:8080/docs")
    print(f"  Reset    : POST http://127.0.0.1:8080/reset")
    print("=" * 60)
    yield


app = FastAPI(
    title="Blackmagic Camera Emulator",
    description="Emulates the Blackmagic camera REST API for development and testing.",
    version="1.0.0",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# CORS — allow all origins so the Flutter web app can connect from any host
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Mount all domain routers under the API prefix
# ---------------------------------------------------------------------------
for router in [
    lens.router,
    video.router,
    transport.router,
    audio.router,
    color.router,
    monitoring.router,
    system.router,
    camera.router,
    slate.router,
    presets.router,
    media.router,
]:
    app.include_router(router, prefix=API_PREFIX)

# ---------------------------------------------------------------------------
# Utility endpoints (no prefix)
# ---------------------------------------------------------------------------

@app.post("/reset", tags=["util"])
def reset_state():
    """Restore all camera state to defaults."""
    state.reset()
    return {"ok": True, "message": "Camera state reset to defaults"}


@app.get("/", tags=["util"])
def root():
    return {
        "name": "Blackmagic Camera Emulator",
        "apiBase": API_PREFIX,
        "docs": "/docs",
    }
