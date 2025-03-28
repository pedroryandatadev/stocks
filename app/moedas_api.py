import requests

# Função para obter todas as moedas disponíveis na API para poder ter mais variedade de escolha
def obter_moedas():
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    resposta = requests.get(url)
    
    if resposta.status_code == 200:
        dados = resposta.json()
        return list(dados['rates'].keys())  # Retorna todas as moedas disponíveis
    else:
        return ['USD', 'EUR', 'BRL']  # Fallback padrão

# Função para converter moeda
def converter_moeda(valor, moeda_origem, moeda_destino):
    url = f'https://api.exchangerate-api.com/v4/latest/{moeda_origem.upper()}'
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
