import React from "react";

export default function StockTable({ stocks, lastUpdated }) {
  if (!stocks || stocks.length === 0) {
    return <p>No penny‑stock data available.</p>;
  }

  return (
    <div className="stock-table-container">
      <div className="header-row">
        <h2>Top Penny Stocks</h2>
        {lastUpdated && (
          <div className="timestamp">As of: {new Date(lastUpdated).toLocaleString()}</div>
        )}
      </div>
      <div className="table-wrapper">
        <table className="stock-table">
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Name</th>
              <th>Price</th>
              <th>% Change</th>
            </tr>
          </thead>
          <tbody>
            {stocks.map((s) => {
              const isPositive = s.percent_change >= 0;
              return (
                <tr key={s.symbol}>
                  <td>{s.symbol}</td>
                  <td>{s.name}</td>
                  <td>${s.price.toFixed(4)}</td>
                  <td className={isPositive ? "positive" : "negative"}>
                    {s.percent_change.toFixed(2)}%
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
