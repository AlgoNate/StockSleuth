import React, { useEffect, useState } from "react";
import "./styles.css";

// GitHub Pages raw JSON URL
const DATA_URL =
  "https://raw.githubusercontent.com/AlgoNate/StockSleuth/main/collector/daily_stock_data.json";

export default function App() {
  const [stocks, setStocks] = useState([]);
  const [lastUpdated, setLastUpdated] = useState(null);

  useEffect(() => {
    fetch(DATA_URL)
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) {
          const latest = data[data.length - 1];
          setStocks(latest.stocks);
          setLastUpdated(latest.timestamp);
        }
      })
      .catch((err) => console.log("Error loading JSON:", err));
  }, []);

  return (
    <div className="container">
      <h1>🔥 Top Penny Stocks</h1>

      {lastUpdated && (
        <div className="updated-box">
          Last Updated: {new Date(lastUpdated).toLocaleString()}
        </div>
      )}

      <table>
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Name</th>
            <th>Price ($)</th>
            <th>Change (%)</th>
          </tr>
        </thead>

        <tbody>
          {stocks.map((s, idx) => (
            <tr key={idx}>
              <td>{s.symbol}</td>
              <td>{s.name}</td>
              <td>${s.price}</td>
              <td className={s.percent_change >= 0 ? "positive" : "negative"}>
                {s.percent_change.toFixed(2)}%
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
