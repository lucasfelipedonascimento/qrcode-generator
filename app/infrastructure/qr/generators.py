from io import BytesIO
from typing import Tuple
import base64
import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from qrcode.image.svg import SvgPathImage
from PIL import Image
from app.domain.entities import QRCodeSpec, OverlaySpec


def _ec_map(level: str):
    if level == "L":
        return ERROR_CORRECT_L
    if level == "M":
        return ERROR_CORRECT_M
    if level == "Q":
        return ERROR_CORRECT_Q
    if level == "H":
        return ERROR_CORRECT_H
    return ERROR_CORRECT_M


def _build_qr(spec: QRCodeSpec) -> qrcode.QRCode:
    qr = qrcode.QRCode(
        version=None,
        error_correction=_ec_map(spec.error_correction),
        box_size=10,
        border=4,
    )
    qr.add_data(spec.text)
    qr.make(fit=True)
    return qr


class QRCodeGenerator:
    def _colors(self, spec: QRCodeSpec) -> Tuple[str, str]:
        return spec.fill_color, spec.background_color

    def _target_size(self, spec: QRCodeSpec) -> Tuple[int, int]:
        w = max(32, int(spec.width))
        h = max(32, int(spec.height))
        return w, h

    def _resize_canvas(self, img: Image.Image, target_w: int, target_h: int, bg: str) -> Image.Image:
        if img.width == target_w and img.height == target_h:
            return img
        canvas = Image.new("RGBA", (target_w, target_h), bg)
        x = (target_w - img.width) // 2
        y = (target_h - img.height) // 2
        canvas.paste(img, (x, y), img if img.mode in ("RGBA", "LA") else None)
        return canvas

    def generate_png(self, spec: QRCodeSpec) -> bytes:
        qr = _build_qr(spec)
        fill, bg = self._colors(spec)
        img = qr.make_image(fill_color=fill, back_color=bg).convert("RGBA")
        target_w, target_h = self._target_size(spec)
        side = min(target_w, target_h)
        if img.width != side or img.height != side:
            img = img.resize((side, side), Image.NEAREST)
        img = self._resize_canvas(img, target_w, target_h, spec.background_color)
        if spec.margin > 0:
            new_w = target_w + 2 * spec.margin
            new_h = target_h + 2 * spec.margin
            bg_img = Image.new("RGBA", (new_w, new_h), spec.background_color)
            bg_img.paste(img, (spec.margin, spec.margin), img)
            img = bg_img
        buf = BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()

    def generate_svg(self, spec: QRCodeSpec) -> str:
        qr = _build_qr(spec)
        fill, bg = self._colors(spec)
        img = qr.make_image(image_factory=SvgPathImage, fill_color=fill, back_color=bg)
        stream = BytesIO()
        img.save(stream)
        svg = stream.getvalue().decode("utf-8")
        return svg

    def generate_png_with_overlay(self, spec: QRCodeSpec, overlay: OverlaySpec, image_bytes: bytes) -> bytes:
        base_png = self.generate_png(spec)
        base_img = Image.open(BytesIO(base_png)).convert("RGBA")
        ov = Image.open(BytesIO(image_bytes)).convert("RGBA")
        if overlay.proportion is not None:
            p = max(0.0, min(1.0, float(overlay.proportion)))
            side = min(base_img.width, base_img.height)
            w = max(1, int(side * p))
            h = max(1, int(side * p))
        elif overlay.image_width and overlay.image_height:
            w, h = int(overlay.image_width), int(overlay.image_height)
        else:
            side = min(base_img.width, base_img.height)
            w = h = max(1, int(side * 0.2))
        ov = ov.resize((w, h), Image.LANCZOS)
        x = (base_img.width - w) // 2
        y = (base_img.height - h) // 2
        base_img.paste(ov, (x, y), ov)
        out = BytesIO()
        base_img.save(out, format="PNG")
        return out.getvalue()
