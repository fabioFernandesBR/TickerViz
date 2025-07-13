from flask import redirect
from flask import jsonify


from flask_openapi3 import OpenAPI, Info, Tag


info = Info(title="TickerViz", version="1.0.0")
app = OpenAPI(__name__, info=info)



#from logger import logger
from schemas import *
from functions import *

from flask_cors import CORS

info = Info(title="TickerViz", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)


# definindo tags
sp500_tag = Tag(name="S&P 500", description="Busca de tickers válidos do índice S&P 500")
ticker_query_tag = Tag(name="Ticker Query", description="Ticker Query")
home_tag = Tag(name="Documentação", description="Swagger")

@app.get('/', tags = [home_tag])
def home():
    """Redireciona para /openapi.
    """
    return redirect('/openapi')


# setor Ticker Query
@app.get('/tickers/sp500/top20', tags=[sp500_tag],
         responses={"200": SchemaTickerList})
def get_top20_sp500_tickers():
    """
    Retorna uma lista de 20 tickers válidos do S&P 500 com seus respectivos nomes.
    """
    return jsonify(get_top20_sp500_tickers_from_txt().model_dump()), 200



## Dados diários das tickers selecionadas
@app.get('/tickers/data', tags=[sp500_tag],
         query=SchemaTickerQueryFlat,
         responses={"200": SchemaFlatList})
def get_flat_data(query: SchemaTickerQueryFlat):
    """
    Retorna dados financeiros diários (últimos 365 dias) como lista plana
    para até 20 tickers fornecidos via query string.
    """
    tickers = [t.upper() for t in query.tickers if t.strip()]
    if len(tickers) < 1:
        return {"error": "Query string 'tickers' não fornecida"}, 400
    if len(tickers) > 20:
        return {"error": "Máximo de 20 tickers permitidos por requisição"}, 400

    flat_data = get_flat_ticker_data(tickers)
    return SchemaFlatList(data=flat_data).model_dump(), 200




@app.get('/tickers/data', tags=[sp500_tag],
         responses={"200": SchemaFlatList})
def get_flat_data(query: SchemaTickerQuery):
    """
    Retorna dados financeiros diários (últimos 365 dias) como lista plana para até 20 tickers fornecidos via query string.
    Exemplo: /tickers/data?tickers=AAPL,MSFT,NVDA
    """
    tickers = [t.upper() for t in query.tickers]
    if len(tickers) < 1:
        return {"error": "Query string 'tickers' não fornecida"}, 400

    if len(tickers) > 20:
        return {"error": "Máximo de 20 tickers permitidos por requisição"}, 400

    flat_data = get_flat_ticker_data(tickers)
    return SchemaFlatList(data=flat_data).model_dump(), 200



