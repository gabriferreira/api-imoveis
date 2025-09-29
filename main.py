from fastapi import FastAPI
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI(title="API de Imóveis")

# Permitir requisições de qualquer lugar (útil para testar no Postman/n8n)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carregar os imóveis do arquivo JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "imoveis.json"), "r", encoding="utf-8") as f:
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
        resultados = [
            i for i in resultados
            if i.get("uuid", "").strip().lower() == uuid.strip().lower()
        ]

    if bairro:
        resultados = [
            i for i in resultados
            if bairro.strip().lower() in i.get("bairro", "").strip().lower()
        ]

    if tipo_imovel:
        resultados = [
            i for i in resultados
            if tipo_imovel.strip().lower() in i.get("tipo_imovel", "").strip().lower()
        ]

    if status:
        resultados = [
            i for i in resultados
            if status.strip().lower() == i.get("status", "").strip().lower()
        ]

    if preco_min is not None:
        resultados = [i for i in resultados if i.get("preco_min", 0) >= preco_min]

    if preco_max is not None:
        resultados = [i for i in resultados if i.get("preco_max", 0) <= preco_max]

    if m2_min is not None:
        resultados = [
            i for i in resultados
            if i.get("detalhe_imovel", {}).get("M2", 0) >= m2_min
        ]

    if m2_max is not None:
        resultados = [
            i for i in resultados
            if i.get("detalhe_imovel", {}).get("M2", 0) <= m2_max
        ]

    if quartos_min is not None:
        resultados = [
            i for i in resultados
            if i.get("detalhe_imovel", {}).get("Quarto", 0) >= quartos_min
        ]

    if quartos_max is not None:
        resultados = [
            i for i in resultados
            if i.get("detalhe_imovel", {}).get("Quarto", 0) <= quartos_max
        ]

    return {"count": len(resultados), "data": resultados}
