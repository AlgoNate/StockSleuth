import React, { useEffect, useState } from "react";
import "./styles.css";

const DATA_URL =
  "https://raw.githubusercontent.com/AlgoNate/StockSleuth/main/collector/daily_stock_data.json";

export default function App() {
  const [stocks, setStocks] = useState([]);
  const [filteredStocks, setFilteredStocks] = useState([]);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");

  // Sorting state
  const [sortConfig, setSortConfig] = useState({
    key: null,
    direction: "asc",
  });

  // Load data
  useEffect(() => {
    fetch(DATA_URL)
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) {
          const latest = data[data.length - 1];
          setStocks(latest.stocks);
          setFilteredStocks(latest.stocks);
          setLastUpdated(latest.timestamp);
        }
      })
      .catch((err) => console.error("Error loading JSON:", err));
  }, []);

  // Handle search
  useEffect(() => {
    const q = searchQuery.toLowerCase();
    const result = stocks.filter(
      (s) =>
        s.symbol.toLowerCase().includes(q) ||
        s.name.toLowerCase().includes(q)
    );
    setFilteredStocks(result);
  }, [searchQuery, stocks]);

  // Sorting function
  const sortBy = (key) => {
    let direction = "asc";

    if (sortConfig.key === key && sortConfig.direction === "asc") {
      direction = "desc";
    }

    const sorted = [...filteredStocks].sort((a, b) => {
      if (key === "symbol" || key === "name") {
        return direction === "asc"
          ? a[key].localeCompare(b[key])
          : b[key].localeCompare(a[key]);
      } else {
        return direction === "asc" ? a[key] - b[key] : b[key] - a[key];
      }
    });

    setSortConfig({ key, direction });
    setFilteredStocks(sorted);
  };

  return (
    <div className="container">
      <h1>🔥 Top Penny Stocks</h1>

      {lastUpdated && (
        <div className="updated-box">
          Last Updated: {new Date(lastUpdated).toLocaleString()}
        </div>
      )}

      {/* 🔍 Search Bar */}
      <input
        type="text"
        className="search-bar"
        placeholder="Search by symbol or company name..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
      />

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
          {filteredStocks.map((s, idx) => (
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

      {filteredStocks.length === 0 && (
        <p className="no-results">No results found.</p>
      )}
    </div>
  );
}
