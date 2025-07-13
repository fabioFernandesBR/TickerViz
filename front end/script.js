let tickersSelecionadas = new Set();
let dadosNaMemoria = {};         // { TICKER: [ { date, open, close, ... } ]}
let cores = {};                  // Consistência por ticker
const campos = ['open', 'close', 'high', 'low', 'volume'];

document.addEventListener("DOMContentLoaded", () => {
  carregarTickers();
});

function carregarTickers() {
  fetch("/tickers/sp500/top20")
    .then(res => res.json())
    .then(data => {
      const container = document.getElementById("tickers-container");
      data.tickers.forEach(obj => {
        const ticker = Object.keys(obj)[0];
        const label = document.createElement("label");
        label.innerHTML = `
          <input type="checkbox" value="${ticker}" onchange="toggleTicker(this)">
          ${ticker}
        `;
        container.appendChild(label);
        cores[ticker] = getCorConsistente(ticker);
      });
    });
}

function toggleTicker(checkbox) {
  const ticker = checkbox.value;
  checkbox.checked
    ? tickersSelecionadas.add(ticker)
    : tickersSelecionadas.delete(ticker);
}

function loadTickerData() {
  if (tickersSelecionadas.size === 0) {
    alert("Selecione ao menos um ticker.");
    return;
  }

  const tickers = Array.from(tickersSelecionadas).filter(t => !dadosNaMemoria[t]);
  if (tickers.length === 0) {
    renderGraficos();
    return;
  }

  fetch(`/tickers/data?tickers=${tickers.join(",")}`)
    .then(res => res.json())
    .then(res => {
      res.data.forEach(entry => {
        if (!dadosNaMemoria[entry.ticker]) dadosNaMemoria[entry.ticker] = [];
        dadosNaMemoria[entry.ticker].push(entry);
      });
      renderGraficos();
    });
}

function recarregarDados() {
  dadosNaMemoria = {};
  loadTickerData();
}

function renderGraficos() {
  const divs = [];

  campos.forEach(campo => {
    const div1 = document.getElementById(`chart-${campo}`);
    const div2 = document.getElementById(`chart-${campo}-pct`);
    renderGrafico(div1, campo);
    renderGraficoPercentual(div2, campo);
    divs.push(div1, div2);
  });

  // Sincronizar zoom e pan entre os gráficos
  divs.forEach(sourceDiv => {
    sourceDiv.on('plotly_relayout', e => {
      divs.forEach(targetDiv => {
        if (targetDiv !== sourceDiv) {
          Plotly.relayout(targetDiv, e);
        }
      });

      // Extrair intervalo de datas para cálculo adicional
      if (e['xaxis.range[0]'] && e['xaxis.range[1]']) {
        const inicio = e['xaxis.range[0]'].slice(0, 10);
        const fim = e['xaxis.range[1]'].slice(0, 10);
        calcularVariacoesNaJanela(inicio, fim);
      }
    });
  });
}

function renderGrafico(div, campo) {
  const traces = [];

  tickersSelecionadas.forEach(ticker => {
    const dados = dadosNaMemoria[ticker];
    const x = dados.map(d => d.date);
    const y = dados.map(d => d[campo]);
    traces.push({
      x, y,
      type: 'scatter',
      mode: 'lines',
      name: ticker,
      line: { color: cores[ticker] }
    });
  });

  Plotly.newPlot(div, traces, {
    title: `${campo.toUpperCase()}`,
    xaxis: { rangeslider: { visible: false }, type: 'date' },
    yaxis: { automargin: true },
    margin: { t: 40 }
  });
}

function renderGraficoPercentual(div, campo) {
  const traces = [];

  tickersSelecionadas.forEach(ticker => {
    const dados = dadosNaMemoria[ticker];
    const x = dados.slice(1).map(d => d.date);
    const y = dados.slice(1).map((d, i) => {
      const anterior = dados[i][campo];
      return anterior ? ((d[campo] / anterior - 1) * 100) : null;
    });

    traces.push({
      x, y,
      type: 'scatter',
      mode: 'lines',
      name: ticker,
      line: { color: cores[ticker] }
    });
  });

  Plotly.newPlot(div, traces, {
    title: `% Variação - ${campo.toUpperCase()}`,
    xaxis: { rangeslider: { visible: false }, type: 'date' },
    yaxis: { title: "%", automargin: true },
    margin: { t: 40 }
  });
}

function calcularVariacoesNaJanela(inicio, fim) {
  tickersSelecionadas.forEach(ticker => {
    const dados = dadosNaMemoria[ticker];
    const inicioIndex = dados.findIndex(d => d.date >= inicio);
    const fimIndex = dados.findIndex(d => d.date >= fim);

    if (inicioIndex >= 0 && fimIndex > inicioIndex) {
      campos.forEach(campo => {
        const ini = dados[inicioIndex][campo];
        const fimVal = dados[fimIndex][campo];
        if (ini && fimVal) {
          const variacao = ((fimVal / ini - 1) * 100).toFixed(2);
          console.log(`${ticker} ${campo}: ${variacao}% entre ${inicio} e ${fim}`);
        }
      });
    }
  });
}

function getCorConsistente(ticker) {
  const base = Math.abs(ticker.split('').reduce((a, b) => a + b.charCodeAt(0), 0));
  return `hsl(${base % 360}, 60%, 50%)`;
}
