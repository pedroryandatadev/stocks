import requests
from dotenv import load_dotenv
import os
import pandas as pd
import datetime
import streamlit as st

# Carregar chave da API
def load_config():
    if 'api' in st.secrets:
        config = {
            'get_alpha_vantage_key': st.secrets['api']['get_alpha_vantage_key']
        }
    else:
        load_dotenv()
        config = {
            'get_alpha_vantage_key': os.getenv('get_alpha_vantage_key')
        }
    return config

config = load_config()
get_alpha_vantage_key = config['get_alpha_vantage_key']

# Função para obter dados mensais não ajustados de ações
def get_stock_data(ticker, start_date, end_date):
    url = (
        f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={ticker}&apikey={get_alpha_vantage_key}&datatype=json'
    )
    
    resposta = requests.get(url)
    
    if resposta.status_code == 200:
        dados = resposta.json()

        if 'Monthly Time Series' in dados:
            series_mensais = dados['Monthly Time Series']

            # Conversão de datas
            start_date_dt = datetime.datetime.strptime(str(start_date), "%Y-%m-%d")
            end_date_dt = datetime.datetime.strptime(str(end_date), "%Y-%m-%d")

            # Filtra dados dentro do intervalo de datas
            data_filtrada = {
                data: info
                for data, info in series_mensais.items()
                if start_date_dt <= datetime.datetime.strptime(data, "%Y-%m-%d") <= end_date_dt
            }

            if data_filtrada:
                df = pd.DataFrame.from_dict(data_filtrada, orient='index')
                df.index = pd.to_datetime(df.index)
                df = df.sort_index()

                # Renomeia colunas para nomes mais legíveis
                df = df.rename(columns={
                    '1. open': 'Open',
                    '2. high': 'High',
                    '3. low': 'Low',
                    '4. close': 'Close',
                    '5. volume': 'Volume'
                })

                # Converte colunas de preço para float
                df[['Open', 'High', 'Low', 'Close']] = df[['Open', 'High', 'Low', 'Close']].astype(float)
                df['Volume'] = df['Volume'].astype(int)

                # Calcula maior e menor valor do período
                highest_valor = df['High'].max()
                lowest_valor = df['Low'].min()

                return df, highest_valor, lowest_valor
            else:
                st.error('Nenhum dado encontrado para o intervalo de datas selecionado.')
                return None, None, None

        else:
            st.error('Erro ao obter os dados da ação. Verifique o ticker ou tente novamente mais tarde.')
            return None, None, None

    else:
        st.error('Erro ao conectar à API. Tente novamente mais tarde.')
        return None, None, None