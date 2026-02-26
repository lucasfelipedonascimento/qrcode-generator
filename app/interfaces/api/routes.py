from fastapi import APIRouter, HTTPException, Response
from base64 import b64encode
from app.interfaces.api.schemas import (
    QRCodeSimplesRequest,
    QRCodeComImagemRequest,
    Base64Response,
)
from app.domain.entities import QRCodeSpec, OverlaySpec
from app.application.services import QRCodeService
from app.infrastructure.qr.generators import QRCodeGenerator
from app.infrastructure.qr.image_fetcher import ImageHTTPFetcher


router = APIRouter()

service = QRCodeService(QRCodeGenerator(), ImageHTTPFetcher())


@router.get("/health", summary="Status da API", tags=["Util"])
def health():
    return {"status": "ok"}


@router.post(
    "/qr/simple",
    summary="Gerar QR Code simples",
    tags=["QR Code"],
)
def gerar_qr_simples(payload: QRCodeSimplesRequest):
    spec = QRCodeSpec(
        text=payload.texto,
        width=payload.largura,
        height=payload.altura,
        margin=payload.margem,
        fill_color=payload.cor_qr,
        background_color=payload.cor_fundo,
        error_correction=payload.nivel_correcao,
        output_format=payload.formato,
    )
    try:
        result = service.generate(spec)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    if isinstance(result, tuple):
        data, mime = result
        if payload.formato == "base64":
            b64 = b64encode(data).decode("utf-8")
            return Base64Response(formato="base64", mime=mime, dados=b64)
        return Response(content=data, media_type=mime, headers={"Content-Disposition": "inline; filename=qr.png"})
    if isinstance(result, str):
        return Response(content=result, media_type="image/svg+xml", headers={"Content-Disposition": "inline; filename=qr.svg"})
    raise HTTPException(status_code=500, detail="Erro ao gerar QR Code")


@router.post(
    "/qr/with-image",
    summary="Gerar QR Code com imagem central",
    tags=["QR Code"],
)
def gerar_qr_com_imagem(payload: QRCodeComImagemRequest):
    spec = QRCodeSpec(
        text=payload.texto,
        width=payload.largura,
        height=payload.altura,
        margin=payload.margem,
        fill_color=payload.cor_qr,
        background_color=payload.cor_fundo,
        error_correction=payload.nivel_correcao,
        output_format=payload.formato,
    )
    overlay = OverlaySpec(
        image_url=str(payload.url_imagem),
        proportion=payload.proporcao_imagem,
        image_width=payload.largura_imagem,
        image_height=payload.altura_imagem,
    )
    if payload.formato == "svg":
        raise HTTPException(status_code=400, detail="Formato svg não suportado com imagem central")
    try:
        data, mime = service.generate_with_image(spec, overlay)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    if payload.formato == "base64":
        b64 = b64encode(data).decode("utf-8")
        return Base64Response(formato="base64", mime=mime, dados=b64)
    return Response(content=data, media_type=mime, headers={"Content-Disposition": "inline; filename=qr.png"})
