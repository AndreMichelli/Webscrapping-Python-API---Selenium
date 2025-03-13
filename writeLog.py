import os, configparser
from datetime import datetime

def escrever_log(mensagem):
    config = configparser.ConfigParser()
    config.read('config.properties')
    base_path = config.get('DEFAULT', 'base_file_path')
    nome_log = base_path + "/log.txt"

    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
    with open(nome_log, 'a') as log_file:
        log_file.write(f"{data_atual} | {mensagem}\n")