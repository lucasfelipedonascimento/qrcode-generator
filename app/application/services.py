from typing import Protocol, Tuple
from . import __init__  # noqa: F401
from app.domain.entities import QRCodeSpec, OverlaySpec


class QRCodeGeneratorPort(Protocol):
    def generate_png(self, spec: QRCodeSpec) -> bytes: ...
    def generate_svg(self, spec: QRCodeSpec) -> str: ...
    def generate_png_with_overlay(self, spec: QRCodeSpec, overlay: OverlaySpec, image_bytes: bytes) -> bytes: ...


class ImageFetcherPort(Protocol):
    def fetch(self, url: str) -> Tuple[bytes, str]: ...


class QRCodeService:
    def __init__(self, generator: QRCodeGeneratorPort, fetcher: ImageFetcherPort):
        self.generator = generator
        self.fetcher = fetcher

    def generate(self, spec: QRCodeSpec) -> Tuple[bytes, str] | str:
        if spec.output_format == "png":
            data = self.generator.generate_png(spec)
            return data, "image/png"
        if spec.output_format == "svg":
            svg = self.generator.generate_svg(spec)
            return svg
        if spec.output_format == "base64":
            data = self.generator.generate_png(spec)
            return data, "image/png"
        data = self.generator.generate_png(spec)
        return data, "image/png"

    def generate_with_image(self, spec: QRCodeSpec, overlay: OverlaySpec) -> Tuple[bytes, str] | str:
        if spec.output_format == "svg":
            raise ValueError("Formato svg com imagem central não suportado")
        img_bytes, _mime = self.fetcher.fetch(overlay.image_url)
        data = self.generator.generate_png_with_overlay(spec, overlay, img_bytes)
        if spec.output_format == "base64":
            return data, "image/png"
        return data, "image/png"
