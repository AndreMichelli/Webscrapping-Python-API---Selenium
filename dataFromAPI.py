import requests, pandas as pd, configparser, sys
from writeLog import escrever_log

try:
    config = configparser.ConfigParser()
    config.read('config.properties')
    escrever_log("iniciando scrapping via API") 
    # api que retorna jogos em promoção
    url = config.get('DEFAULT', 'api_cheapshark_url')
    base_path = config.get('DEFAULT', 'base_file_path')
    file_path = base_path + "/Ofertas_jogos.csv"

    response = requests.get(url)
    # print(response)
    # print(response.status_code)
    if(response.status_code == 200):
        escrever_log("dados retornados com sucesso") 
        dados = response.json()
        # print(dados)
        dados_selecionados = []
        for item in dados:
            nome = item["title"]
            preco_promo = item["salePrice"]
            preco_padrao = item["normalPrice"]
            pctg_desconto = item["savings"]

            dados_selecionados.append([nome, preco_promo, preco_padrao, pctg_desconto])
            # print(nome + " | " + preco_padrao + " | " + preco_promo)

        colunas = ["Titulo", "Oferta", "Preco padrao", "Porcentagem do desconto"]
        df = pd.DataFrame(dados_selecionados, columns=colunas)
        df.to_csv(file_path, index=False, encoding="utf-8")
        escrever_log("Arquivo gerado")
    else:
        raise "Erro na requisição | Código retornado: " + response.status_code
except Exception as e:
    linha_erro = sys.exc_info()[-1].tb_lineno
    escrever_log("Erro na linha " + str(linha_erro) + "- Erro: " + str(e))