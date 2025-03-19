import yfinance as yf

# Função para obter os dados da ação (Codigo açõa, data inicio e data final)
def get_stock_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)

    if data.empty:
        return None, None, None  # Retorna None se não houver dados

    highest_valor = data['High'].max()
    lowest_valor = data['Low'].min()

    return data, highest_valor, lowest_valor