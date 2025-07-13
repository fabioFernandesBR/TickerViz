from pydantic import BaseModel
from pydantic import RootModel
from typing import List


# Seção das Classes - isso define o formato da API


class SchemaTicker(RootModel[dict[str, str]]):
    """Representa um ticker e seu nome, como {'AAPL': 'Apple Inc.'}"""
    pass

class SchemaTickerList(BaseModel):
    """Lista de tickers válidos com seus respectivos nomes."""
    tickers: List[SchemaTicker]


class SchemaTickerQuery(BaseModel):
    tickers: List[str]

class SchemaTickerQueryFlat(BaseModel):
    """Recebe lista de tickers via query string"""
    tickers: List[str] = ["AAPL", "MSFT", "NVDA"]



class SchemaDailyFlat(BaseModel):
    """Representa um registro diário de mercado para um ticker"""
    ticker: str
    date: str
    open: float
    close: float
    high: float
    low: float
    volume: int


class SchemaFlatList(BaseModel):
    data: List[SchemaDailyFlat]



class SchemaMensagemErro(BaseModel):
    """ Define como uma mensagem de erro será representada
    """
    message: str = "Algo deu ruim"
