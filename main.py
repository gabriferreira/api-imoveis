from fastapi import FastAPI, Query
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import json
from pathlib import Path

app = FastAPI(title="API de Imóveis")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carregar base do JSON
BASE_PATH = Path(__file__).parent
with open(BASE_PATH / "imoveis.json", "r", encoding="utf-8") as f:
    imoveis = json.load(f)

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
        resultados = [i for i in resultados if i.get("uuid") == uuid]

    if bairro:
        resultados = [i for i in resultados if bairro.lower() in i.get("bairro", "").lower()]

    if tipo_imovel:
        resultados = [i for i in resultados if tipo_imovel.lower() == i.get("tipo_imovel", "").lower()]

    if status:
        resultados = [i for i in resultados if status.lower() == i.get("status", "").lower()]

    if preco_min is not None:
        resultados = [i for i in resultados if i.get("preco_min") is not None and i["preco_min"] >= preco_min]

    if preco_max is not None:
        resultados = [i for i in resultados if i.get("preco_max") is not None and i["preco_max"] <= preco_max]

    if m2_min is not None:
        resultados = [i for i in resultados if i.get("detalhe_imovel", {}).get("M2") is not None and i["detalhe_imovel"]["M2"] >= m2_min]

    if m2_max is not None:
        resultados = [i for i in resultados if i.get("detalhe_imovel", {}).get("M2") is not None and i["detalhe_imovel"]["M2"] <= m2_max]

    if quartos_min is not None:
        resultados = [i for i in resultados if i.get("detalhe_imovel", {}).get("Quarto") is not None and i["detalhe_imovel"]["Quarto"] >= quartos_min]

    if quartos_max is not None:
        resultados = [i for i in resultados if i.get("detalhe_imovel", {}).get("Quarto") is not None and i["detalhe_imovel"]["Quarto"] <= quartos_max]

    return {"count": len(resultados), "data": resultados}
