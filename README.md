# API de Geração de QR Codes (Arquitetura Hexagonal)

API construída em Python com FastAPI para gerar QR Codes:
- Sem imagem central.
- Com imagem central a partir de uma URL, controlando tamanho ou proporção.
- Suporte a formatos: PNG, SVG e Base64 (PNG codificado).
- Parâmetros de cores, margem, tamanho e nível de correção de erros.

Observação: QR Codes são intrinsecamente quadrados; se largura e altura diferirem, a imagem será centralizada no canvas solicitado.

## Arquitetura

Arquitetura hexagonal, separando:
- `domain`: entidades de domínio.
- `application`: orquestração via serviço e portas.
- `infrastructure`: implementações de geradores e fetcher de imagens.
- `interfaces/api`: rotas, esquemas e FastAPI.

## Requisitos

Instale Python 3.11+.

### Clonar o projeto

Baixe o projeto para sua máquina e entre na pasta:
```
git clone <URL_DO_REPOSITORIO>
cd API Gerar QR Code
```

### Ambiente e dependências

Windows PowerShell:
```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Executando a API

```
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

OBS: Se não funcionar, tente atualizar o pip:
```pip install --upgrade pip

Abra a documentação interativa:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

- `GET /health` – Status da API.
- `POST /qr/simple` – Gera QR Code simples.
- `POST /qr/with-image` – Gera QR Code com imagem central.

Todos os endpoints possuem descrição no Swagger, em Português.

### Parâmetros comuns

No corpo JSON:
- `texto` (str) – Texto a codificar.
- `largura` (int) – Largura final em px.
- `altura` (int) – Altura final em px.
- `margem` (int) – Margem externa em px.
- `cor_qr` (hex) – Cor do QR, padrão `#000000`.
- `cor_fundo` (hex) – Cor do fundo, padrão `#FFFFFF`.
- `formato` (png|svg|base64) – Formato de saída.
- `nivel_correcao` (L|M|Q|H) – Correção de erro.

Para `/qr/with-image`:
- `url_imagem` (URL) – URL da imagem central.
- `proporcao_imagem` (0.0–1.0) – Proporção do lado do QR.
- `largura_imagem`, `altura_imagem` (int) – Tamanho fixo da imagem central.

Regra: informe `proporcao_imagem` ou largura/altura da imagem. Se nenhum for informado, usa 20% por padrão.

Limitação: `formato = "svg"` com imagem central não é suportado; use `png` ou `base64`.

### Exemplos

QR simples em PNG:
```
curl -X POST http://localhost:8000/qr/simple \
  -H "Content-Type: application/json" \
  -o qr.png \
  -d '{
    "texto":"Olá mundo",
    "largura":256,
    "altura":256,
    "margem":0,
    "cor_qr":"#000000",
    "cor_fundo":"#FFFFFF",
    "formato":"png",
    "nivel_correcao":"M"
  }'
```

QR simples em SVG:
```
curl -X POST http://localhost:8000/qr/simple \
  -H "Content-Type: application/json" \
  -o qr.svg \
  -d '{
    "texto":"Exemplo SVG",
    "largura":256,
    "altura":256,
    "formato":"svg",
    "margem":0,
    "cor_qr":"#000000",
    "cor_fundo":"#FFFFFF",
    "nivel_correcao":"M"
  }'
```

QR com imagem central (PNG):
```
curl -X POST http://localhost:8000/qr/with-image \
  -H "Content-Type: application/json" \
  -o qr_com_imagem.png \
  -d '{
    "texto":"Com imagem",
    "largura":512,
    "altura":512,
    "margem":0,
    "cor_qr":"#000000",
    "cor_fundo":"#FFFFFF",
    "formato":"png",
    "nivel_correcao":"M",
    "url_imagem":"https://exemplo.com/logo.png",
    "proporcao_imagem":0.3
  }'
```

Base64:
```
curl -X POST http://localhost:8000/qr/simple \
  -H "Content-Type: application/json" \
  -d '{
    "texto":"Base64",
    "largura":256,
    "altura":256,
    "formato":"base64"
  }'
```

## Testes

Execute:
```
pytest -q
```

Cobertura de:
- Unidade do gerador (PNG, SVG, overlay).
- Rotas principais.

## Observações de uso

- Tamanho: QR é quadrado; se `largura != altura`, o QR é centralizado no canvas.
- Margem: aplicada como padding externo em pixels.
- Cores: informar em hexadecimal no formato `#RRGGBB`.
- Imagens centrais: recomenda-se usar proporções moderadas (ex.: 0.2–0.35) e níveis de correção M, Q ou H.
