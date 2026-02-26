from typing import Optional, Literal
from pydantic import BaseModel, Field, HttpUrl, field_validator


class QRCodeBase(BaseModel):
    texto: str = Field(..., description="Texto que será codificado no QR Code")
    largura: int = Field(256, ge=16, le=4096, description="Largura final em pixels")
    altura: int = Field(256, ge=16, le=4096, description="Altura final em pixels")
    margem: int = Field(0, ge=0, le=512, description="Margem externa em pixels")
    cor_qr: str = Field("#000000", pattern="^#([0-9a-fA-F]{6})$", description="Cor do QR em hex")
    cor_fundo: str = Field("#FFFFFF", pattern="^#([0-9a-fA-F]{6})$", description="Cor de fundo em hex")
    formato: Literal["png", "svg", "base64"] = Field("png", description="Formato de saída")
    nivel_correcao: Literal["L", "M", "Q", "H"] = Field("M", description="Nível de correção de erros")


class QRCodeSimplesRequest(QRCodeBase):
    pass


class QRCodeComImagemRequest(QRCodeBase):
    url_imagem: HttpUrl = Field(..., description="URL da imagem central")
    proporcao_imagem: Optional[float] = Field(None, ge=0.0, le=1.0, description="Proporção da imagem central")
    largura_imagem: Optional[int] = Field(None, ge=1, le=4096, description="Largura da imagem central")
    altura_imagem: Optional[int] = Field(None, ge=1, le=4096, description="Altura da imagem central")

    @field_validator("proporcao_imagem")
    @classmethod
    def check_size_fields(cls, v, info):
        return v


class Base64Response(BaseModel):
    formato: str
    mime: str
    dados: str
