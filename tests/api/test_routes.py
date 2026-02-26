from fastapi.testclient import TestClient
from app.main import app
import base64
from PIL import Image
from io import BytesIO
import types


client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_qr_simple_png():
    payload = {
        "texto": "teste",
        "largura": 256,
        "altura": 256,
        "margem": 0,
        "cor_qr": "#000000",
        "cor_fundo": "#FFFFFF",
        "formato": "png",
        "nivel_correcao": "M",
    }
    r = client.post("/qr/simple", json=payload)
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("image/png")
    assert r.content[:8] == b"\x89PNG\r\n\x1a\n"


def test_qr_simple_svg():
    payload = {
        "texto": "svg",
        "largura": 256,
        "altura": 256,
        "formato": "svg",
        "margem": 0,
        "cor_qr": "#000000",
        "cor_fundo": "#FFFFFF",
        "nivel_correcao": "M",
    }
    r = client.post("/qr/simple", json=payload)
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("image/svg+xml")
    assert r.text.strip().startswith("<svg")


def test_qr_simple_base64():
    payload = {
        "texto": "base64",
        "largura": 256,
        "altura": 256,
        "formato": "base64",
        "margem": 0,
        "cor_qr": "#000000",
        "cor_fundo": "#FFFFFF",
        "nivel_correcao": "M",
    }
    r = client.post("/qr/simple", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["formato"] == "base64"
    b = base64.b64decode(data["dados"])
    assert b[:8] == b"\x89PNG\r\n\x1a\n"


def test_qr_with_image_png(monkeypatch):
    from app.infrastructure.qr import image_fetcher

    def fake_get(url, timeout=5.0, stream=True):
        img = Image.new("RGBA", (40, 40), (0, 128, 255, 255))
        buf = BytesIO()
        img.save(buf, format="PNG")
        class Resp:
            status_code = 200
            headers = {"Content-Type": "image/png"}
            content = buf.getvalue()
            def raise_for_status(self): pass
        return Resp()

    monkeypatch.setattr(image_fetcher.requests, "get", fake_get)

    payload = {
        "texto": "com-imagem",
        "largura": 256,
        "altura": 256,
        "margem": 0,
        "cor_qr": "#000000",
        "cor_fundo": "#FFFFFF",
        "formato": "png",
        "nivel_correcao": "M",
        "url_imagem": "http://exemplo/imagem.png",
        "proporcao_imagem": 0.3,
    }
    r = client.post("/qr/with-image", json=payload)
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("image/png")
    assert r.content[:8] == b"\x89PNG\r\n\x1a\n"

