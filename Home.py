from app.moedas_api import obter_moedas, converter_moeda
from app.acoes_yfinance import get_stock_data
import streamlit as st

st.set_page_config(page_title='Ações', page_icon='img//icon-grafico.ico', layout='wide')

# Sidebar da Página
with st.container():
    st.sidebar.image('img//logo-consulta-acoes.png')

    st.sidebar.title('Conversor de Moedas')

    # Obter todas as moedas disponíveis
    moedas_disponiveis = obter_moedas()

    # Selectbox dos tipos de moedas e valor a ser convertido
    moeda_origem = st.sidebar.selectbox('Moeda de origem:', moedas_disponiveis, index=moedas_disponiveis.index('USD'))
    moeda_destino = st.sidebar.selectbox('Moeda de destino:', moedas_disponiveis, index=moedas_disponiveis.index('BRL'))
    valor = st.sidebar.number_input('Valor a converter:', min_value=1.00, step=1.00)

    # Checkbox para exibir a taxa de câmbio
    mostrar_taxa = st.sidebar.checkbox('Mostrar taxa de câmbio')

    # Botão de conversão de moeda
    if st.sidebar.button('Converter'):
        valor_convertido, taxa = converter_moeda(valor, moeda_origem, moeda_destino)

        if valor_convertido is not None:
            st.sidebar.success(f"{valor:.2f} {moeda_origem} equivale a {valor_convertido:.2f} {moeda_destino}")

            if mostrar_taxa:
                st.sidebar.info(f'Taxa de câmbio: 1 {moeda_origem} = {taxa:.2f} {moeda_destino}')
        else:
            st.sidebar.error('Erro: Moeda não encontrada ou serviço indisponível!')

# Interface principal (ações)
with st.container():
    st.title('Consulta de Ações')

    st.write('Este aplicativo permite consultar o histórico de preços de ações e calcular o retorno de investimentos.')
    st.write('Os valores de cotação e gráficos retornam na moeda original em que a ação está cadastrada, caso consulte a AAPL(ação da Apple) os valores retornam em dólar, se consultar a PETR4.SA(ação da Petrobras) os valores retornam em real brasileiro.')

    col1, col2, col3 = st.columns([2, 1, 1])  
    # Primeira linha de inputs seleção de ação, data de início e data de fim
    with col1:
        ticker = st.text_input('Digite o código da ação (ex: AAPL, MSFT, TSLA):', 'AAPL')
    with col2:
        start_date = st.date_input('Escolha a data de início:')
    with col3:
        end_date = st.date_input('Escolha a data de fim:')

    with col1:
        valor_inicial = st.number_input('Digite o investimento inicial:', min_value=1.00, step=1.00)

    # Verificando se os dados necessários foram preenchidos
    if ticker and start_date and end_date:
        data, highest_valor, lowest_valor = get_stock_data(ticker, start_date, end_date)

        if data is not None and not data.empty:
            # Obter o preço inicial (primeiro fechamento) e final (último fechamento)
            valor_investido_inicial = data['Close'].iloc[0]  # Preço no início
            valor_investido_final = data['Close'].iloc[-1]  # Preço no final

            # Calculando o retorno em porcentagem
            retorno_investimento = (valor_investido_final - valor_investido_inicial) / valor_investido_inicial * 100

            # Cálculo do valor final do investimento
            valor_final = valor_inicial * (1 + retorno_investimento / 100)

            # Exibição do retono do investimento e valor final ao lado o input de digitação do valor
            with col2:
                st.metric(label='Retorno do investimento: ', value=f"{retorno_investimento:.2f}%")
            with col3:
                st.metric(label='Valor final do investimento: ', value=f"{valor_final:.2f}")

            # Linha da maior e menor cotação do periodo consultada
            with col1:
                st.metric(label='Menor cotação do período', value=f"{lowest_valor:.2f}")
            with col3:
                st.metric(label='Maior cotação do período', value=f"{highest_valor:.2f}")

            # Gráficos de linha
            st.write('Gráfico de fechamento')
            st.line_chart(data['Close'])

            st.write('Gráfico de comparação de picos')
            st.line_chart(data[['Close', 'High', 'Low']])

        else:
            st.warning('Nenhum dado encontrado para o período selecionado. Verifique o código da ação e as datas.')