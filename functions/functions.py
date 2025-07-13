import pandas as pd
from schemas.schemas import SchemaTicker, SchemaTickerList

from pytickersymbols import PyTickerSymbols
import yfinance as yf

from pathlib import Path


# Função para ler os 500 maiores do S&P 500 a partir do PyTickerSymbols
def get_all_sp500_tickers_with_names() -> SchemaTickerList:
    """
    Retorna todos os tickers do índice S&P500 com seus respectivos nomes,
    validando via yfinance.
    """
    stock_data = PyTickerSymbols()
    sp500_stocks = stock_data.get_stocks_by_index("S&P 500")

    tickers_validos = []
    for stock in sp500_stocks:
        symbol = stock.get('symbol')
        name = stock.get('name')
        try:
            info = yf.Ticker(symbol).fast_info
            if info and "last_price" in info:
                tickers_validos.append(SchemaTicker({symbol: name}))
        except Exception:
            continue

    return SchemaTickerList(tickers=tickers_validos)



# Função para ler os 20 maiores do S&P 500 a partir do txt
def get_top20_sp500_tickers_from_txt(path: str = "top_sp500.txt") -> SchemaTickerList:
    """
    Lê uma lista estática das 20 maiores empresas do S&P500 a partir de um arquivo .txt,
    valida cada ticker via yfinance, e retorna a lista formatada como SchemaTickerList.
    """
    tickers_validos = []

    # Constrói o caminho absoluto do arquivo em relação ao arquivo atual
    path = Path(__file__).parent.parent / "top_sp500.txt"

    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                if ":" in line:
                    symbol, name = line.strip().split(":", 1)
                    symbol = symbol.strip()
                    symbol_yf = symbol.replace('.', '-')
                    name = name.strip()
                    print(line)
                    print(symbol)
                    print(name)
                    try:
                        yf_data = yf.Ticker(symbol_yf).info
                        print(yf_data)
                        if yf_data and 'regularMarketPrice' in yf_data:
                            tickers_validos.append(SchemaTicker({symbol: name}))
                    except Exception:
                        continue
    except FileNotFoundError:
        print(f"Arquivo '{path}' não encontrado.")
    
    return SchemaTickerList(tickers=tickers_validos)

import yfinance as yf
from datetime import datetime, timedelta
from schemas.schemas import SchemaDailyFlat

def get_flat_ticker_data(ticker_list: list[str]) -> list[SchemaDailyFlat]:
    """
    Retorna uma lista plana de dados diários para múltiplos tickers dos últimos 365 dias.
    """
    end_date = datetime.today().strftime("%Y-%m-%d")
    start_date = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d")

    all_data = []

    for ticker in ticker_list[:20]:  # Limite de 20
        try:
            history = yf.Ticker(ticker).history(start=start_date, end=end_date)
            for date, row in history.iterrows():
                all_data.append(SchemaDailyFlat(
                    ticker=ticker,
                    date=date.strftime("%Y-%m-%d"),
                    open=row["Open"],
                    close=row["Close"],
                    high=row["High"],
                    low=row["Low"],
                    volume=int(row["Volume"])
                ))
        except Exception:
            continue

    return all_data
