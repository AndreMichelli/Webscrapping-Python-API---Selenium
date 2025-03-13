import pandas as pd, time, configparser, sys
from writeLog import escrever_log
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

try:
    config = configparser.ConfigParser()
    config.read('config.properties')
    url = config.get('DEFAULT', 'api_ML_url')
    
    base_path = config.get('DEFAULT', 'base_file_path')
    file_path = base_path + "/Ofertas.csv"

    driver = webdriver.Chrome() # busca webdriver do chrome

    driver.get(url)
    time.sleep(10)

    produtos = driver.find_elements(By.CLASS_NAME, 'poly-card__content')
    # print(produtos)
    dados = []
    escrever_log("buscando os dados no site")
    for produto in produtos:
        nome_produto = produto.find_element(By.CLASS_NAME, 'poly-component__title').text
        try:
            vendedor = produto.find_element(By.CLASS_NAME, 'poly-component__seller').text
            vendedor.replace("Por ", "")
        except NoSuchElementException:
            # print("vendedor nao identificado: " + nome_produto)
            vendedor = "vendedor nao identificado"
            pass
        
        moeda = produto.find_element(By.CLASS_NAME, 'andes-money-amount__currency-symbol').text
        valor = produto.find_element(By.CLASS_NAME, 'andes-money-amount__fraction').text
        try:
            centavos = produto.find_element(By.CLASS_NAME, 'andes-money-amount__cents').text
            preco = moeda + " " + valor + "," + centavos

        except NoSuchElementException:
            # print("valor sem centavos: " + nome_produto)
            preco = moeda + " " + valor 
            pass

        try:
            frete = produto.find_element(By.CLASS_NAME, "poly-component__shipping").text
        except NoSuchElementException:
            # print("não tem frete gratis: " + nome_produto)
            frete = ""
            pass
        
        link =  produto.find_element(By.CLASS_NAME, 'poly-component__title').get_attribute("href")
        # print(link)

        dados.append([nome_produto, vendedor, preco, frete, link])

    driver.quit()

    escrever_log("gerando arquivo csv")
    colunas = ["Nome", "Vendedor", "Preço", "Frete", "Link da oferta"]
    df = pd.DataFrame(dados, columns=colunas)
    df.to_csv(file_path, index=False, encoding="utf-8")
except Exception as e:
    linha_erro = sys.exc_info()[-1].tb_lineno
    escrever_log("Erro na linha " + str(linha_erro) + "- Erro: " + str(e))