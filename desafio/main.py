import json
import csv
import re
from datetime import datetime
from openpyxl import Workbook


# 1. LEITURA DOS ARQUIVOS

def ler_json(caminho_json):
    '''Lê o arquivo JSON e retorna o dicionário.'''
    with open(caminho_json, 'r', encoding='utf-8') as arq:
        return json.load(arq)

def ler_csv(caminho_csv):
    '''Lê o arquivo CSV e retorna uma lista de dicionários.'''
    with open(caminho_csv, 'r', encoding='utf-8') as arq:
        vendas = []
        leitor = csv.DictReader(arq)

        for l in leitor:
            vendas.append(l)
        
        return vendas
    
#2. LIMPEZA DOS DADOS

def limpar_nome_filias(nome):
    '''Remove caracteres indesejados e corrige nomes de cidades.'''
    nome = re.sub(r"[^a-zA-Zá-úÁ-ÚçÇ ]", "", nome).strip()

    #Correções específicas (adicionando erros comuns)
    correcoes = {
        "Joinvile": "Joinville",
        "Florianopólis": "Florianópolis",
        "Blumenauu": "Blumenau",
        "Chapekó": "Chapecó",
        "Crisiuma": "Criciúma"
    }

    return correcoes.get(nome, nome)

def limpar_vendas(vendas):
    '''Remove registros inválidos e limpa nomes de filiais.'''
    vendas_limpas = []

    for v in vendas:
        if not v['id_produto'] or not v['quantidade']:
            continue #Ignorar os registros incompletos

        v['filial'] = limpar_nome_filias(v['filial'])
        vendas_limpas.append(v)
    
    return vendas_limpas

#3. Integração de dados

def integrar_dados(vendas, produtos):
    '''Une os dados de vendas e produtos com base no id_produto'''
    produtos_dict = {p["id"]: p for p in produtos} 
    relatorio = []

    for v in vendas:
        id_prod = int(v["id_produto"])
        produto = produtos_dict.get(id_prod)

        if not produtos:
            continue #Se não encontrarmos o produto

        preco = float(produto["preco"])
        quantidade = int(v["quantidade"])
        valor_total = round(preco * quantidade, 2)

        #Converter data de string para datetime
        data_venda = datetime.strptime(v["data_venda"], "%Y-%m-%d")

        relatorio.append({
            "id_venda": v["id_venda"],
            "id_produto": id_prod,
            "nome_produto": produto["nome"],
            "filial": v["filial"],
            "quantidade": quantidade,
            "preco_unitario": preco,
            "valor_total_venda": valor_total,
            "data_venda": data_venda.strftime("%Y-%m-%d"),
            "dia_semana": data_venda.strftime("%A"),
            "mes": data_venda.strftime("%B"),
            "ano": data_venda.year
        })
    return relatorio


# 4. EXPORTAÇÃO CVS

def salvar_csv(dados, nome_arquivo):
    """Salva os dados tratados em um arquivo CSV."""
    campos = [
        "id_venda", "id_produto", "nome_produto", "filial",
        "quantidade", "preco_unitario", "valor_total_venda",
        "data_venda", "dia_semana", "mes", "ano"
    ]

    with open(nome_arquivo, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(dados)

    print(f"Arquivo CSV '{nome_arquivo}' gerado com sucesso.")

#5. EXPORTAÇÃO EXCEL

def salvar_resumo_excel(dados, nome_arquivo):
    """Gera um arquivo Excel com resumo de vendas por produto e filial."""
    wb = Workbook()
    ws_filial = wb.active
    ws_filial.title = "Resumo por Filial"

    # Cabeçalho
    ws_filial.append(["Filial", "Total de Vendas (R$)"])

    # Cálculo dO total por filial
    total_por_filial = {}
    for item in dados:
        total_por_filial[item["filial"]] = total_por_filial.get(item["filial"], 0) + item["valor_total_venda"]

    for filial, total in total_por_filial.items():
        ws_filial.append([filial, round(total, 2)])

    # Nova aba: Resumo por Produto
    ws_produto = wb.create_sheet("Resumo por Produto")
    ws_produto.append(["Produto", "Total Vendido (R$)"])

    total_por_produto = {}
    for item in dados:
        nome_prod = item["nome_produto"]
        total_por_produto[nome_prod] = total_por_produto.get(nome_prod, 0) + item["valor_total_venda"]

    for produto, total in total_por_produto.items():
        ws_produto.append([produto, round(total, 2)])

    # Aba com total geral
    ws_total = wb.create_sheet("Total Geral")
    valor_total = sum(item["valor_total_venda"] for item in dados)
    ws_total.append(["Valor Total de Vendas (R$)"])
    ws_total.append([round(valor_total, 2)])

    wb.save(nome_arquivo)
    print(f"Arquivo Excel '{nome_arquivo}' gerado com sucesso.")


#6. EXECUÇÃO PRINCIPAL

def main():
    # Leitura dos arquivos de entrada
    produtos_json = ler_json("produtos.json")
    produtos = produtos_json["produtos"]
    vendas = ler_csv("vendas.csv")

    # Limpeza e integração
    vendas_limpas = limpar_vendas(vendas)
    relatorio = integrar_dados(vendas_limpas, produtos)

    # Exportação
    salvar_csv(relatorio, "relatorio_vendas.csv")

    data_atual = datetime.now().strftime("%Y-%m-%d")
    salvar_resumo_excel(relatorio, f"relatorio_resumo_{data_atual}.xlsx")


if __name__ == "__main__":
    main()



