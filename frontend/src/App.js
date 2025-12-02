import React, { useEffect, useState } from "react";

export default function App() {
  const [stocks, setStocks] = useState([]);

  useEffect(() => {
    fetch(
      "https://algonate.github.io/StockSleuth/collector/daily_stock_data.json"
    )
      .then((res) => res.json())
      .then((data) => {
        if (data.length > 0) {
          const latest = data[data.length - 1];
          setStocks(latest.stocks || []);
        }
      });
  }, []);

  return (
    <div style={{ fontFamily: "Arial", padding: "20px" }}>
      <h1>Penny Stock Screener</h1>
      <table border="1" cellPadding="8" style={{ borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Name</th>
            <th>Price ($)</th>
          </tr>
        </thead>
        <tbody>
          {stocks.map((s, i) => (
            <tr key={i}>
              <td>{s.symbol}</td>
              <td>{s.name}</td>
              <td>{s.price}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
