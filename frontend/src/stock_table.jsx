import React, { useState, useEffect } from "react";
import { Sparklines, SparklinesLine } from "react-sparklines";
import "./stock_table.css"; // keep your CSS file

export default function StockTable({ stocks, lastUpdated }) {
  const [filter, setFilter] = useState("");
  const [sortConfig, setSortConfig] = useState({ key: "symbol", direction: "asc" });
  const [localTime, setLocalTime] = useState(
    lastUpdated ? new Date(lastUpdated) : new Date()
  );

  useEffect(() => {
    if (lastUpdated) {
      setLocalTime(new Date(lastUpdated));
    }
  }, [lastUpdated]);

  const minutesAgo = Math.floor((new Date() - localTime) / 60000);

  const sortedStocks = [...stocks].sort((a, b) => {
    const { key, direction } = sortConfig;
    let aValue = a[key];
    let bValue = b[key];

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

  const requestSort = (key) => {
    let direction = "asc";
    if (sortConfig.key === key && sortConfig.direction === "asc") direction = "desc";
    setSortConfig({ key, direction });
  };

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
              <th>Trend</th> {/* New sparkline column */}
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
                  <td>
                    {s.price_history ? (
                      <Sparklines data={s.price_history} width={100} height={20}>
                        <SparklinesLine color={isPositive ? "green" : "red"} />
                      </Sparklines>
                    ) : (
                      "—"
                    )}
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
