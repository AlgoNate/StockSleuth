import React, { useEffect, useState } from "react";
import "./styles.css";

const DATA_URL =
  "https://raw.githubusercontent.com/AlgoNate/StockSleuth/main/collector/daily_stock_data.json";

export default function App() {
  const [stocks, setStocks] = useState([]);
  const [filteredStocks, setFilteredStocks] = useState([]);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [darkMode, setDarkMode] = useState(false);
  const [loading, setLoading] = useState(true); // NEW
  const [error, setError] = useState(null); // NEW

  const [sortConfig, setSortConfig] = useState({
    key: null,
    direction: "asc",
  });

  useEffect(() => {
    fetch(DATA_URL)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to load stock data.");
        return res.json();
      })
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) {
          const latest = data[data.length - 1];
          setStocks(latest.stocks);
          setFilteredStocks(latest.stocks);
          setLastUpdated(latest.timestamp);
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error loading data:", err);
        setError("⚠ Unable to load data. Please check GitHub or try again later.");
        setLoading(false);
      });
  }, []);

  // Search
  useEffect(() => {
    const q = searchQuery.toLowerCase();
    const result = stocks.filter(
      (s) =>
        s.symbol.toLowerCase().includes(q) ||
        s.name.toLowerCase().includes(q)
    );
    setFilteredStocks(result);
  }, [searchQuery, stocks]);

  const sortBy = (key) => {
    let direction = "asc";
    if (sortConfig.key === key && sortConfig.direction === "asc") {
      direction = "desc";
    }

    const sorted = [...filteredStocks].sort((a, b) =>
      key === "symbol" || key === "name"
        ? direction === "asc"
          ? a[key].localeCompare(b[key])
          : b[key].localeCompare(a[key])
        : direction === "asc"
        ? a[key] - b[key]
        : b[key] - a[key]
    );

    setSortConfig({ key, direction });
    setFilteredStocks(sorted);
  };

  return (
    <div className={darkMode ? "container dark" : "container"}>
      <div className="header-row">
        <h1>🔥 Top Penny Stocks</h1>
        <button className="dark-toggle" onClick={() => setDarkMode(!darkMode)}>
          {darkMode ? "☀ Light Mode" : "🌙 Dark Mode"}
        </button>
      </div>

      {/* ERROR BANNER */}
      {error && <div className="error-banner">{error}</div>}

      {/* Last Updated */}
      {!loading && lastUpdated && (
        <div className="updated-box">
          Last Updated: {new Date(lastUpdated).toLocaleString()}
        </div>
      )}

      {/* Search */}
      {!loading && (
        <input
          type="text"
          className="search-bar"
          placeholder="Search by symbol or company name..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      )}

      {/* LOADING SKELETON */}
      {loading && (
        <div className="skeleton-wrapper">
          <div className="skeleton-row"></div>
          <div className="skeleton-row"></div>
          <div className="skeleton-row"></div>
          <div className="skeleton-row"></div>
        </div>
      )}

      {/* TABLE */}
      {!loading && (
        <div className="table-wrapper">
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
        </div>
      )}

      {!loading && filteredStocks.length === 0 && (
        <p className="no-results">No results found.</p>
      )}
    </div>
  );
}
