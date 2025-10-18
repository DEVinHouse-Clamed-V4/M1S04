with open("vendas.csv", "r", encoding="utf-8") as arq:
    vendas = {}
    for linha in arq.readlines()[1:]:
        data, produto, quantidade, valor = linha.strip().split(",")
        quantidade = int(quantidade)
        valor = float(valor)
        if produto not in vendas:
            vendas[produto] = {"total_vendido": 0,  "valor_total": 0.0}
        vendas[produto]["total_vendido"] += quantidade
        vendas[produto]["valor_total"] += valor * quantidade

with open("relatorio.csv", "w", encoding="utf-8") as arq:
    arq.write("produto,total_vendido,valor_total\n")
    for produto, info in vendas.items():
        arq.write(f"{produto}, {info["total_vendido"]},{info["valor_total"]}\n")


import json

ARQUIVO_JSON = "dados.json"

dados = {"empresa": "Clamed", "ano": 2025, "produtos": ["Shampoo", "Sabonete"]}
with open(ARQUIVO_JSON, "w", encoding="utf-8") as arq:
    json.dump(dados, arq, indent=4, ensure_ascii=False)

with open(ARQUIVO_JSON, "r", encoding="utf-8") as arq:
    conteudo = json.load(arq)
    print(conteudo["produtos"])




