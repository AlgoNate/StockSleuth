import React, { useEffect, useState } from "react";
import "./styles.css";

const DATA_URL =
  "https://raw.githubusercontent.com/AlgoNate/StockSleuth/main/collector/daily_stock_data.json";

export default function App() {
  const [stocks, setStocks] = useState([]);
  const [lastUpdated, setLastUpdated] = useState(null);

  // Sorting State
  const [sortConfig, setSortConfig] = useState({
    key: null,
    direction: "asc",
  });

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
      .catch((err) => console.error("Error loading JSON:", err));
  }, []);

  // Sorting function
  const sortBy = (key) => {
    let direction = "asc";

    // If clicking the same column, reverse direction
    if (sortConfig.key === key && sortConfig.direction === "asc") {
      direction = "desc";
    }

    const sorted = [...stocks].sort((a, b) => {
      if (key === "symbol" || key === "name") {
        // String sort
        return direction === "asc"
          ? a[key].localeCompare(b[key])
          : b[key].localeCompare(a[key]);
      } else {
        // Number sort
        return direction === "asc" ? a[key] - b[key] : b[key] - a[key];
      }
    });

    setSortConfig({ key, direction });
    setStocks(sorted);
  };

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
            <th onClick={() => sortBy("symbol")}>Symbol ⬍</th>
            <th onClick={() => sortBy("name")}>Name ⬍</th>
            <th onClick={() => sortBy("price")}>Price ($) ⬍</th>
            <th onClick={() => sortBy("percent_change")}>Change (%) ⬍</th>
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
