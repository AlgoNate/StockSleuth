import React, { useEffect, useState } from "react";

// URL to your GitHub Pages JSON file
const DATA_URL = "https://algonate.github.io/StockSleuth/collector/daily_stock_data.json";

// Table component to display top movers
function TopMoversTable({ stocks }) {
  if (!stocks || stocks.length === 0) return <p>No data available.</p>;

  return (
    <table style={{ width: "100%", borderCollapse: "collapse" }}>
      <thead>
        <tr>
          <th style={{ border: "1px solid black", padding: "8px" }}>Symbol</th>
          <th style={{ border: "1px solid black", padding: "8px" }}>Name</th>
          <th style={{ border: "1px solid black", padding: "8px" }}>Price ($)</th>
          <th style={{ border: "1px solid black", padding: "8px" }}>Change (%)</th>
        </tr>
      </thead>
      <tbody>
        {stocks.map((stock) => (
          <tr key={stock.symbol}>
            <td style={{ border: "1px solid black", padding: "8px" }}>{stock.symbol}</td>
            <td style={{ border: "1px solid black", padding: "8px" }}>{stock.name}</td>
            <td style={{ border: "1px solid black", padding: "8px" }}>{stock.price.toFixed(2)}</td>
            <td
              style={{
                border: "1px solid black",
                padding: "8px",
                color: stock.percent_change >= 0 ? "green" : "red",
              }}
            >
              {stock.percent_change.toFixed(2)}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

function App() {
  const [stocks, setStocks] = useState([]);
  const [timestamp, setTimestamp] = useState("");

  useEffect(() => {
    fetch(DATA_URL)
      .then((res) => res.json())
      .then((data) => {
        if (data.length > 0) {
          // Use the latest entry (last item in array)
          const latest = data[data.length - 1];
          setStocks(latest.stocks);
          setTimestamp(latest.timestamp);
        }
      })
      .catch((err) => console.error("Error fetching data:", err));
  }, []);

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>Top Penny Stocks</h1>
      {timestamp && <p>Data as of: {new Date(timestamp).toLocaleString()}</p>}
      <TopMoversTable stocks={stocks} />
    </div>
  );
}

export default App;
