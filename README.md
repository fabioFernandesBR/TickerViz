# TickerViz
Visualization of Stock Market data - select and download data from web and manipulate data locally

## Purpose
Assess the performance of JavaScript to perform calculations on Front End, based on interactive charts.

## Strategy
Implement the following architecture: Front End <---> Back End <---> Yahoo Finance
- Yahoo Finance provides financial data via API.
- Back End requests data to Yahoo Finance API and provide it to Front End, as Front End requests.
- Front End:
  1. Requests Ticker to be visualized.
  2. Execute local calculations via JavaScript (day-by-day % growth, taking as day 0 the day selected by user in the interactive chart).
  3. Display data in interactive charts.
So, once data is transferred to Front End, the calculations should be fast, allowing continuous display of downloaded and calculated data.



### To create and activate virtual environment
to create: python -m venv .venv
to activate: .\.venv\Scripts\activate

### To install dependencies
pip install -r requirements.txt

### To run locally
flask run --host 0.0.0.0 --port 5000 --reload
