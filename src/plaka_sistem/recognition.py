from dataclasses import dataclass
import re
from typing import Optional

import httpx


PLATE_REGEX = re.compile(r"\b\d{2}\s?[A-Z]{1,3}\s?\d{2,4}\b")


@dataclass
class PlateRecognitionResult:
    plate: Optional[str]
    source: str
    raw_text: str


class CloudPlateRecognizer:
    def __init__(self, endpoint: str = "", api_key: str = ""):
        self.endpoint = endpoint
        self.api_key = api_key

    async def recognize(self, image_base64: Optional[str], text_hint: Optional[str] = None) -> PlateRecognitionResult:
        if self.endpoint and image_base64:
            headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(
                    self.endpoint,
                    headers=headers,
                    json={"image_base64": image_base64},
                )
                response.raise_for_status()
                payload = response.json()
                raw_text = payload.get("text", "")
                plate = _extract_plate(raw_text)
                return PlateRecognitionResult(plate=plate, source="cloud", raw_text=raw_text)

        raw_text = text_hint or ""
        plate = _extract_plate(raw_text)
        return PlateRecognitionResult(plate=plate, source="hint", raw_text=raw_text)


def _extract_plate(text: str) -> Optional[str]:
    match = PLATE_REGEX.search(text.upper())
    if not match:
        return None
    return "".join(match.group(0).split())
