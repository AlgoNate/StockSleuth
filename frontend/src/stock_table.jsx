import React, { useState, useEffect } from "react";

export default function StockTable({ stocks, lastUpdated }) {
  const [localTime, setLocalTime] = useState(
    lastUpdated ? new Date(lastUpdated).toLocaleString() : null
  );

  // Update localTime whenever lastUpdated changes
  useEffect(() => {
    if (lastUpdated) {
      setLocalTime(new Date(lastUpdated).toLocaleString());
    }
  }, [lastUpdated]);

  if (!stocks || stocks.length === 0) {
    return <p>No penny‑stock data available.</p>;
  }

  return (
    <div className="stock-table-container">
      <div className="header-row">
        <h2>Top Penny Stocks</h2>
        {localTime && <div className="timestamp">As of: {localTime}</div>}
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
