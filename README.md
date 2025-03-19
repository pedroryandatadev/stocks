<p align="center">
  <img src="img/logo-consulta-acoes.png" alt="Consulto logo" width="300">
</p>

Esse projeto realiza a visualização de valores e do desempenho de ações de acordo com o período de tempo especificado.

Nesse projeto existem blocos de comparação de valores e gráficos de progresso e comparação, além de um calculador de investimento.

<p align="center">
  <img src="previews/preview-interface.png" alt="Interface do projeto" >
</p>

# APi & Dados

Foram utilizados duas fontes de dados sendo elas a biblioteca `yfinance` do yahoo para uso das ações, para as moedas a api do `Exchangerate-API`.

- Documentação da biblioteca [yfinance](https://pypi.org/project/yfinance/).

- Documentação da Api [Exchangerate-API](https://www.exchangerate-api.com/docs/overview)


## Funções utilizadas 

- Seletor e conversor de moedas
- Visualizador de taxa de câmbio (moeda)
- Input de ações
- Seleção de datas inicio e fim
- Projetor de investimento com retorno do percentual mais valor final
- Indicadores de menor e maior cotação 
- Gráfico de desempenho ao longo do tempo
- Gráfico de comparação alta e baixa ao longo do tempo
<p align="center">
  <img src="previews/preview-fuction.png" alt="Funções" >
</p>

# Requerimentos

Uso das bibliotecas `requests`, `yfinance` e `streamlit`.

Instalação pode ser feita pelo requirements.txt para evitar conflitos de versões:

``` 

    pip install -r requirements.txt

```

### Créditos

> Desenvolvimento e design por [pedroryandatadev (Pedro Ryan)](https://github.com/pedroryandatadev) 