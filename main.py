from fastapi import FastAPI, Query
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API de Imóveis")

# Permitir requisições de qualquer lugar (útil para testar no Postman/n8n)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base de exemplo (você pode substituir por leitura de JSON real)
imoveis = [
    {
        "uuid": "ac51cb5a-c388-4de3-82df-f406fb0dfdaa",
        "name": "GS Stay Praia da Costa",
        "bairro": "Praia da Costa",
        "tipo_imovel": "Apartamento",
        "status": "DISPONIVEL",
        "preco_min": 671073.90,
        "preco_max": 1105362.83,
        "detalhe_imovel": {"M2": 24, "Banheiro": 1, "Garagem": 1},
        "municipio": {"name": "Vila Velha", "uf": "ES"},
    },
    {
        "uuid": "7ae610ad-539f-4d1c-9fc8-af483931bae5",
        "name": "Verve",
        "bairro": "Jardim Camburí",
        "tipo_imovel": "Apartamento",
        "status": "DISPONIVEL",
        "preco_min": 1639458.85,
        "preco_max": 2358206.34,
        "detalhe_imovel": {"M2": 88, "Quarto": 3, "Suite": 1, "Banheiro": 2, "Garagem": 2},
        "municipio": {"name": "Vitória", "uf": "ES"},
    },
    # adicione mais imóveis aqui
]

@app.get("/imoveis")
def listar_imoveis(
    uuid: Optional[str] = None,
    bairro: Optional[str] = None,
    tipo_imovel: Optional[str] = None,
    status: Optional[str] = None,
    preco_min: Optional[float] = None,
    preco_max: Optional[float] = None,
    m2_min: Optional[float] = None,
    m2_max: Optional[float] = None,
    quartos_min: Optional[int] = None,
    quartos_max: Optional[int] = None
):
    resultados = imoveis

    if uuid:
        resultados = [i for i in resultados if i["uuid"] == uuid]

    if bairro:
        resultados = [i for i in resultados if bairro.lower() in i.get("bairro","").lower()]

    if tipo_imovel:
        resultados = [i for i in resultados if tipo_imovel.lower() == i.get("tipo_imovel","").lower()]

    if status:
        resultados = [i for i in resultados if status.lower() == i.get("status","").lower()]

    if preco_min is not None:
        resultados = [i for i in resultados if i.get("preco_min",0) >= preco_min]

    if preco_max is not None:
        resultados = [i for i in resultados if i.get("preco_max",0) <= preco_max]

    if m2_min is not None:
        resultados = [i for i in resultados if i.get("detalhe_imovel", {}).get("M2",0) >= m2_min]

    if m2_max is not None:
        resultados = [i for i in resultados if i.get("detalhe_imovel", {}).get("M2",0) <= m2_max]

    if quartos_min is not None:
        resultados = [i for i in resultados if i.get("detalhe_imovel", {}).get("Quarto",0) >= quartos_min]

    if quartos_max is not None:
        resultados = [i for i in resultados if i.get("detalhe_imovel", {}).get("Quarto",0) <= quartos_max]

    return {"count": len(resultados), "data": resultados}
