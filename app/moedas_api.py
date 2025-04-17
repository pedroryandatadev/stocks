import requests
from dotenv import load_dotenv
import os
import streamlit as st

# Função para carregar as configurações da API
# Verifica se o aplicativo está sendo executado no Streamlit Cloud ou localmente
def load_config():
    
    if 'api' in st.secrets:
        # Está no Streamlit Cloud (st.secrets tem a seção [api])
        config = {
            'get_moeda_key': st.secrets['api']['get_moeda_key'], # Chave da API para obter as moedas registrada no secrets
            'converter_moeda_key': st.secrets['api']['converter_moeda_key'] # Chave da API para converter moedas registrada no secrets
        }
    else:
        # Está local (carrega do .env)
        load_dotenv()
        config = {
            'get_moeda_key': os.getenv('get_moeda_key'), # Chave da API para obter as moedas disponíveis
            'converter_moeda_key': os.getenv('converter_moeda_key') # Chave da API para converter moedas
        }
    
    return config

config = load_config()

get_moeda_key = config['get_moeda_key']
converter_moeda_key = config['converter_moeda_key']

# Função para obter todas as moedas disponíveis na API para poder ter mais variedade de escolha
def obter_moedas():
    url = get_moeda_key
    resposta = requests.get(url)
    
    if resposta.status_code == 200:
        dados = resposta.json()
        return list(dados['rates'].keys())  # Retorna todas as moedas disponíveis
    else:
        return ['USD', 'EUR', 'BRL']  # Fallback padrão

# Função para converter moeda
def converter_moeda(valor, moeda_origem, moeda_destino):
    url = f'{converter_moeda_key}{moeda_origem.upper()}'
    resposta = requests.get(url)
    
    if resposta.status_code != 200:
        return None, None
    
    dados_moeda = resposta.json()

    if moeda_destino.upper() in dados_moeda['rates']:
        taxa = dados_moeda['rates'][moeda_destino.upper()] # Obtem a taxa de câmbio
        valor_convertido = valor * taxa # Calculo da conversão do valor final
        return round(valor_convertido, 2), taxa
    else:
        return None, None
