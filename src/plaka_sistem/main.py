from fastapi import FastAPI
from pydantic import BaseModel

from .config import settings
from .direction import DirectionGate
from .recognition import CloudPlateRecognizer

app = FastAPI(title="Tek Taraflı Geçiş Plaka Tanıma")

gate = DirectionGate(
    allowed_direction=settings.allowed_direction,
    enter_line_x=settings.enter_line_x,
    exit_line_x=settings.exit_line_x,
    min_delta_x=settings.min_delta_x,
)
recognizer = CloudPlateRecognizer(settings.ocr_endpoint, settings.ocr_api_key)


class IngestRequest(BaseModel):
    camera_id: str
    track_id: str
    centroid_x: float
    image_base64: str | None = None
    ocr_text_hint: str | None = None


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ingest")
async def ingest(payload: IngestRequest) -> dict:
    allowed = gate.process(payload.track_id, payload.centroid_x)
    if not allowed:
        return {
            "camera_id": payload.camera_id,
            "track_id": payload.track_id,
            "allowed": False,
            "reason": "direction_not_validated",
        }

    result = await recognizer.recognize(payload.image_base64, payload.ocr_text_hint)
    return {
        "camera_id": payload.camera_id,
        "track_id": payload.track_id,
        "allowed": True,
        "plate": result.plate,
        "ocr_source": result.source,
        "raw_text": result.raw_text,
    }
