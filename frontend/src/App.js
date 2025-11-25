import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import "chart.js/auto";

function App() {
  const [history, setHistory] = useState([]);
  const DATA_URL =
    "https://raw.githubusercontent.com/AlgoNate/StockSleuth/main/collector/daily_stock_data.json";

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await fetch(DATA_URL);
        const data = await response.json();
        setHistory(data || []);
      } catch (err) {
        console.error("Error fetching stock data:", err);
        setHistory([]);
      }
    }

    fetchData();
    const interval = setInterval(fetchData, 60 * 1000); // Refresh every 1 minute
    return () => clearInterval(interval);
  }, []);

  if (!history.length) return <div>Loading stock data...</div>;

  // Last run = most recent
  const lastRun = history[history.length - 1];
  const topStocks = (lastRun?.stocks || []).filter((s) => s.price <= 1); // Only penny stocks

  // Symbols for chart
  const symbols = Array.from(
    new Set(
      history.flatMap((run) =>
        (run.stocks || [])
          .filter((s) => s.price <= 1) // Filter penny stocks
          .map((s) => s.symbol)
      )
    )
  ).slice(0, 25);

  // Chart datasets
  const datasets = symbols.map((symbol) => {
    const stockHistory = history.map((run) => {
      const found = (run.stocks || []).find(
        (s) => s.symbol === symbol && s.price <= 1
      );
      return found ? found.price : null;
    });

    const lastStock = (lastRun.stocks || []).find(
      (s) => s.symbol === symbol && s.price <= 1
    );
    const percentChange = lastStock ? lastStock.percent_change : 0;
    const lineColor = percentChange >= 0 ? "green" : "red";

    return {
      label: symbol,
      data: stockHistory,
      fill: false,
      borderColor: lineColor,
      backgroundColor: lineColor,
      tension: 0.3,
      pointRadius: 4,
      pointHoverRadius: 6,
    };
  });

  const labels = history.map((run) =>
    new Date(run.timestamp).toLocaleTimeString()
  );

  const chartData = { labels, datasets };

  const chartOptions = {
    plugins: {
      tooltip: {
        callbacks: {
          label: function (context) {
            const symbol = context.dataset.label;
            const price = context.parsed.y;
            const runIndex = context.dataIndex;
            const percent =
              (history[runIndex].stocks || [])
                .filter((s) => s.price <= 1)
                .find((s) => s.symbol === symbol)?.percent_change ?? 0;
            return `${symbol}: $${price} (${percent}%)`;
          },
        },
      },
      legend: { display: true, position: "bottom" },
    },
    scales: {
      y: { title: { display: true, text: "Price ($)" } },
      x: { title: { display: true, text: "Time" } },
    },
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h2>Top 25 Penny Stocks Today</h2>

      {/* Top Movers Table */}
      <table
        style={{ width: "100%", borderCollapse: "collapse", marginBottom: "2rem" }}
      >
        <thead>
          <tr>
            <th style={{ borderBottom: "1px solid #ccc", textAlign: "left" }}>
              Symbol
            </th>
            <th style={{ borderBottom: "1px solid #ccc", textAlign: "left" }}>
              Name
            </th>
            <th style={{ borderBottom: "1px solid #ccc", textAlign: "right" }}>
              Price
            </th>
            <th style={{ borderBottom: "1px solid #ccc", textAlign: "right" }}>
              Change %
            </th>
          </tr>
        </thead>
        <tbody>
          {topStocks.map((s) => (
            <tr key={s.symbol}>
              <td>{s.symbol}</td>
              <td>{s.name}</td>
              <td style={{ textAlign: "right" }}>${s.price}</td>
              <td
                style={{
                  textAlign: "right",
                  color: s.percent_change >= 0 ? "green" : "red",
                  fontWeight: "bold",
                }}
              >
                {s.percent_change}%
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Intraday Chart */}
      <Line data={chartData} options={chartOptions} />
    </div>
  );
}

export default App;
