import json
import re

def parse_float(valor_str):
    """
    Converte string de preço ou número em float.
    Ex: "R$ 1.639.458,85" -> 1639458.85
    """
    if not valor_str:
        return None
    # Remove "R$", espaços, troca vírgula por ponto decimal
    valor_limpo = re.sub(r'[R$\s]', '', valor_str).replace('.', '').replace(',', '.')
    try:
        return float(valor_limpo)
    except ValueError:
        return None

def parse_faixa(faixa_str):
    """
    Converte faixa "3 a 4" ou "24 a 72" em tupla (min, max)
    """
    if not faixa_str:
        return (None, None)
    numeros = re.findall(r'\d+', faixa_str)
    if len(numeros) == 1:
        n = int(numeros[0])
        return (n, n)
    elif len(numeros) >= 2:
        return (int(numeros[0]), int(numeros[1]))
    else:
        return (None, None)

def normalize_imovel(imovel):
    """
    Normaliza campos importantes do imovel para filtragem e uso.
    """
    detalhe = imovel.get("detalhe_imovel", {})

    # Faixas numéricas
    m2_min, m2_max = parse_faixa(detalhe.get("M2"))
    quarto_min, quarto_max = parse_faixa(detalhe.get("Quarto"))
    suite_min, suite_max = parse_faixa(detalhe.get("Suite"))
    banheiro_min, banheiro_max = parse_faixa(detalhe.get("Banheiro"))
    garagem_min, garagem_max = parse_faixa(detalhe.get("Garagem"))

    # Preços
    preco_min = parse_float(imovel.get("preco_min"))
    preco_max = parse_float(imovel.get("preco_max"))

    # Status
    status = imovel.get("status") or imovel.get("status_imovel")

    return {
        "uuid": imovel.get("uuid"),
        "name": imovel.get("name"),
        "modalidade_oferta": imovel.get("modalidade_oferta"),
        "rcod": imovel.get("rcod"),
        "tipo_imovel": imovel.get("tipo_imovel"),
        "descricao": imovel.get("descricao"),
        "m2_min": m2_min,
        "m2_max": m2_max,
        "quarto_min": quarto_min,
        "quarto_max": quarto_max,
        "suite_min": suite_min,
        "suite_max": suite_max,
        "banheiro_min": banheiro_min,
        "banheiro_max": banheiro_max,
        "garagem_min": garagem_min,
        "garagem_max": garagem_max,
        "preco_min": preco_min,
        "preco_max": preco_max,
        "bairro": imovel.get("bairro"),
        "bairro_cidade": imovel.get("bairro_cidade"),
        "prazo_entrega": imovel.get("prazo_entrega"),
        "status": status,
        "file": imovel.get("file"),
        "files": imovel.get("files", []),
        "site": imovel.get("site"),
        "municipio": imovel.get("municipio", {}),
        "caracteristicas": imovel.get("caracteristicas", {}),
        "ranking": imovel.get("ranking")
    }

def load_imoveis(json_path):
    """
    Carrega o JSON do seu arquivo e normaliza cada imovel.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Seu JSON vem aninhado: {"json": {"data": [...]}}
    imoveis_raw = data.get("json", {}).get("data", [])
    imoveis = [normalize_imovel(imovel) for imovel in imoveis_raw]
    return imoveis

def filtrar_imoveis(imoveis, preco_max=None, m2_min=None, quartos_min=None):
    """
    Exemplo de filtro: preço máximo, m2 mínimo, quartos mínimos
    """
    resultado = []
    for imovel in imoveis:
        if preco_max and (imovel["preco_max"] is None or imovel["preco_max"] > preco_max):
            continue
        if m2_min and (imovel["m2_min"] is None or imovel["m2_min"] < m2_min):
            continue
        if quartos_min and (imovel["quarto_min"] is None or imovel["quarto_min"] < quartos_min):
            continue
        resultado.append(imovel)
    return resultado

if __name__ == "__main__":
    # Exemplo de uso
    imoveis = load_imoveis("imoveis.json")
    print(f"Total de imóveis carregados: {len(imoveis)}")

    # Filtra por preço até 2 milhões, m2 mínimo 70 e 3 quartos
    filtrados = filtrar_imoveis(imoveis, preco_max=2000000, m2_min=70, quartos_min=3)
    print(f"Imóveis filtrados: {len(filtrados)}")
    for im in filtrados:
        print(f"{im['name']} - {im['preco_min']} a {im['preco_max']} - {im['quarto_min']} quartos")
