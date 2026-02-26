from app.infrastructure.qr.generators import QRCodeGenerator
from app.domain.entities import QRCodeSpec, OverlaySpec
from PIL import Image
from io import BytesIO


def test_generate_png_basic():
    gen = QRCodeGenerator()
    spec = QRCodeSpec(text="hello", width=256, height=256)
    data = gen.generate_png(spec)
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    assert len(data) > 100


def test_generate_svg_basic():
    gen = QRCodeGenerator()
    spec = QRCodeSpec(text="hello-svg", width=256, height=256, output_format="svg")
    svg = gen.generate_svg(spec)
    assert svg.strip().startswith("<svg")
    assert "path" in svg


def test_generate_png_with_overlay():
    gen = QRCodeGenerator()
    spec = QRCodeSpec(text="with-overlay", width=256, height=256)
    img = Image.new("RGBA", (64, 64), (255, 0, 0, 255))
    buf = BytesIO()
    img.save(buf, format="PNG")
    ov = OverlaySpec(image_url="http://example.com/image.png", proportion=0.3)
    out = gen.generate_png_with_overlay(spec, ov, buf.getvalue())
    assert out[:8] == b"\x89PNG\r\n\x1a\n"
    assert len(out) > 100
