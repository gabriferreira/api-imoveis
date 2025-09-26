from fastapi import FastAPI, Query
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI(title="API de Imóveis")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(BASE_DIR, "imoveis.json")

def valor(dic, *chaves, default=0):
    v = dic
    for k in chaves:
        v = v.get(k, {})
    return v if isinstance(v, (int, float)) else default

try:
    with open(json_path, "r", encoding="utf-8") as f:
        imoveis = json.load(f)
except FileNotFoundError:
    imoveis = []
    print("Arquivo imoveis.json não encontrado. Lista de imóveis vazia.")

@app.get("/imoveis")
def listar_imoveis(
    uuid: Optional[str] = None,
    name: Optional[str] = None,
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

    if name:
        resultados = [i for i in resultados if name.lower() in i.get("name", "").lower()]

    if bairro:
        resultados = [i for i in resultados if bairro.lower() in i.get("bairro", "").lower()]

    if tipo_imovel:
        resultados = [i for i in resultados if tipo_imovel.lower() == i.get("tipo_imovel", "").lower()]

    if status:
        resultados = [i for i in resultados if status.lower() == i.get("status", "").lower()]

    if preco_min is not None:
        resultados = [i for i in resultados if valor(i, "preco_min") >= preco_min]

    if preco_max is not None:
        resultados = [i for i in resultados if valor(i, "preco_max") <= preco_max]

    if m2_min is not None:
        resultados = [i for i in resultados if valor(i, "detalhe_imovel", "M2") >= m2_min]

    if m2_max is not None:
        resultados = [i for i in resultados if valor(i, "detalhe_imovel", "M2") <= m2_max]

    if quartos_min is not None:
        resultados = [i for i in resultados if valor(i, "detalhe_imovel", "Quarto") >= quartos_min]

    if quartos_max is not None:
        resultados = [i for i in resultados if valor(i, "detalhe_imovel", "Quarto") <= quartos_max]

    return {"count": len(resultados), "data": resultados}
