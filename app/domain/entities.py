from dataclasses import dataclass
from typing import Optional, Literal


ErrorCorrection = Literal["L", "M", "Q", "H"]
OutputFormat = Literal["png", "svg", "base64"]


@dataclass
class QRCodeSpec:
    text: str
    width: int
    height: int
    margin: int = 4
    fill_color: str = "#000000"
    background_color: str = "#FFFFFF"
    error_correction: ErrorCorrection = "M"
    output_format: OutputFormat = "png"


@dataclass
class OverlaySpec:
    image_url: str
    proportion: Optional[float] = None
    image_width: Optional[int] = None
    image_height: Optional[int] = None
