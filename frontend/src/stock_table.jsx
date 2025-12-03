import React, { useState, useEffect } from "react";
import "./stock_table.css"; // We'll create this CSS file next

export default function StockTable({ stocks, lastUpdated }) {
  const [filter, setFilter] = useState("");
  const [sortConfig, setSortConfig] = useState({ key: "symbol", direction: "asc" });
  const [localTime, setLocalTime] = useState(
    lastUpdated ? new Date(lastUpdated) : new Date()
  );

  // Update local time whenever lastUpdated changes
  useEffect(() => {
    if (lastUpdated) {
      setLocalTime(new Date(lastUpdated));
    }
  }, [lastUpdated]);

  // Compute "minutes ago"
  const minutesAgo = Math.floor((new Date() - localTime) / 60000);

  // Sorting function
  const sortedStocks = [...stocks].sort((a, b) => {
    const { key, direction } = sortConfig;
    let aValue = a[key];
    let bValue = b[key];

    // Handle numeric sort for price and percent_change
    if (key === "price" || key === "percent_change") {
      aValue = parseFloat(aValue);
      bValue = parseFloat(bValue);
    } else {
      aValue = aValue.toString().toLowerCase();
      bValue = bValue.toString().toLowerCase();
    }

    if (aValue < bValue) return direction === "asc" ? -1 : 1;
    if (aValue > bValue) return direction === "asc" ? 1 : -1;
    return 0;
  });

  // Handle column header click for sorting
  const requestSort = (key) => {
    let direction = "asc";
    if (sortConfig.key === key && sortConfig.direction === "asc") direction = "desc";
    setSortConfig({ key, direction });
  };

  // Filter stocks based on search input
  const filteredStocks = sortedStocks.filter(
    (s) =>
      s.symbol.toLowerCase().includes(filter.toLowerCase()) ||
      s.name.toLowerCase().includes(filter.toLowerCase())
  );

  if (!stocks || stocks.length === 0) {
    return <p>No penny‑stock data available.</p>;
  }

  return (
    <div className="stock-table-container">
      <div className="header-row">
        <h2>Top Penny Stocks</h2>
        <div className="timestamp">
          As of: {localTime.toLocaleString()} ({minutesAgo} min ago)
        </div>
      </div>

      <div className="controls">
        <input
          type="text"
          placeholder="Search by symbol or name..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="search-input"
        />
      </div>

      <div className="table-wrapper">
        <table className="stock-table">
          <thead>
            <tr>
              <th onClick={() => requestSort("symbol")}>Symbol</th>
              <th onClick={() => requestSort("name")}>Name</th>
              <th onClick={() => requestSort("price")}>Price</th>
              <th onClick={() => requestSort("percent_change")}>% Change</th>
            </tr>
          </thead>
          <tbody>
            {filteredStocks.map((s) => {
              const isPositive = s.percent_change >= 0;
              return (
                <tr key={s.symbol}>
                  <td>{s.symbol}</td>
                  <td>{s.name}</td>
                  <td className="numeric">${s.price.toFixed(4)}</td>
                  <td className={`numeric ${isPositive ? "positive" : "negative"}`}>
                    {isPositive ? "▲" : "▼"} {s.percent_change.toFixed(2)}%
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
