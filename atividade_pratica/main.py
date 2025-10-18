import json
import csv

INPUT_JSON = "atividade_pratica/produtos.json"

ARCHIVE_CSV = "atividade_pratica/produtos.csv"

ARCHIVE_CSV_NEW = "atividade_pratica/produtos_new.csv"

#Ler json
with open(INPUT_JSON, "r", encoding="utf-8") as arq:
   dados = json.load(arq)

produtos = dados.get("produtos", [])  #dados["produtos"]

with open(ARCHIVE_CSV, "w", encoding="utf-8") as arq:
    campos = ["id", "nome", "preco", "estoque"]
    escritor = csv.DictWriter(arq, fieldnames=campos)

    escritor.writeheader()

    for p in produtos:
        escritor.writerow({
            "id": p.get('id'),
            "nome": p.get('nome'),
            "preco": f"{p.get('preco'):.2f}",
            "estoque": p.get('estoque')
        })

print(f"Arquivo {ARCHIVE_CSV} criado com sucesso!")

# Proposta: Gerar um novo arquivo com uma nova coluna valor_estoque(preco * estoque)

with open(ARCHIVE_CSV_NEW, "w", encoding="utf-8") as arq:
    campos = ["id", "nome", "preco", "estoque", "valor_estoque"]
    escritor = csv.DictWriter(arq, fieldnames=campos)

    escritor.writeheader()

    for p in produtos:
        preco = float(p.get('preco'))
        estoque = int(p.get('estoque'))
        valor_estoque = round((preco * estoque), 2)

        escritor.writerow({
            "id": p.get('id'),
            "nome": p.get('nome'),
            "preco": f"{p.get('preco'):.2f}",
            "estoque": p.get('estoque'),
            "valor_estoque": valor_estoque
        })

print(f"Arquivo {ARCHIVE_CSV_NEW} criado com sucesso!")