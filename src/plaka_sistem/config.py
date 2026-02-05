from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    allowed_direction: str = os.getenv("ALLOWED_DIRECTION", "left_to_right")
    enter_line_x: int = int(os.getenv("ENTER_LINE_X", "120"))
    exit_line_x: int = int(os.getenv("EXIT_LINE_X", "380"))
    min_delta_x: int = int(os.getenv("MIN_DELTA_X", "120"))
    ocr_endpoint: str = os.getenv("OCR_ENDPOINT", "")
    ocr_api_key: str = os.getenv("OCR_API_KEY", "")


settings = Settings()
