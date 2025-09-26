import json
import os

# Caminho para o JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(BASE_DIR, "imoveis.json")

# Carrega o JSON
with open(json_path, "r", encoding="utf-8") as f:
    imoveis = json.load(f)

# Mostra o primeiro imóvel para ver todos os campos
print(json.dumps(imoveis[0], indent=4, ensure_ascii=False))
