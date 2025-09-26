from fastapi import FastAPI, Query
import json

app = FastAPI()

# Carrega o JSON com os imóveis
with open("imoveis.json", "r", encoding="utf-8") as f:
    imoveis = json.load(f)

@app.get("/imoveis")
def buscar_imoveis(
    name: str = None,
    uuid: str = None,
    modalidade_oferta: str = None,
    status: str = None,
    tipo_imovel: str = None,
    descricao: str = None,
    detalhe_imovel: str = None,
    preco_min: float = None,
    preco_max: float = None,
    bairro: str = None,
    bairro_cidade: str = None,
    prazo_entrega: str = None,
    site: str = None,
    municipio: str = None,
    caracteristicas: str = None,
    CONDOMINIO: str = None,
    LOCALIZACAO: str = None,
    limit: int = 10
):
    resultados = imoveis

    # Filtros
    if name:
        resultados = [i for i in resultados if name.lower() in str(i.get("name", "")).lower()]
    if uuid:
        resultados = [i for i in resultados if uuid.lower() in str(i.get("uuid", "")).lower()]
    if modalidade_oferta:
        resultados = [i for i in resultados if modalidade_oferta.lower() in str(i.get("modalidade_oferta", "")).lower()]
    if status:
        resultados = [i for i in resultados if status.lower() in str(i.get("status", "")).lower()]
    if tipo_imovel:
        resultados = [i for i in resultados if tipo_imovel.lower() in str(i.get("tipo_imovel", "")).lower()]
    if descricao:
        resultados = [i for i in resultados if descricao.lower() in str(i.get("descricao", "")).lower()]
    if detalhe_imovel:
        resultados = [i for i in resultados if detalhe_imovel.lower() in str(i.get("detalhe_imovel", "")).lower()]
    if preco_min:
        resultados = [i for i in resultados if i.get("preco_min") is not None and i.get("preco_min") >= preco_min]
    if preco_max:
        resultados = [i for i in resultados if i.get("preco_max") is not None and i.get("preco_max") <= preco_max]
    if bairro:
        resultados = [i for i in resultados if bairro.lower() in str(i.get("bairro", "")).lower()]
    if bairro_cidade:
        resultados = [i for i in resultados if bairro_cidade.lower() in str(i.get("bairro_cidade", "")).lower()]
    if prazo_entrega:
        resultados = [i for i in resultados if prazo_entrega.lower() in str(i.get("prazo_entrega", "")).lower()]
    if site:
        resultados = [i for i in resultados if site.lower() in str(i.get("site", "")).lower()]
    if municipio:
        resultados = [i for i in resultados if municipio.lower() in str(i.get("municipio", "")).lower()]
    if caracteristicas:
        resultados = [i for i in resultados if caracteristicas.lower() in str(i.get("caracteristicas", "")).lower()]
    if CONDOMINIO:
        resultados = [i for i in resultados if CONDOMINIO.lower() in str(i.get("CONDOMINIO", "")).lower()]
    if LOCALIZACAO:
        resultados = [i for i in resultados if LOCALIZACAO.lower() in str(i.get("LOCALIZACAO", "")).lower()]

    # Limita a quantidade de resultados
    return resultados[:limit]
