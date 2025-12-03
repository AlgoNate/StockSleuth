import React, { useEffect, useState } from "react";

function StockTable() {
  const [watchlist, setWatchlist] = useState([]);
  const [stockData, setStockData] = useState({});

  useEffect(() => {
    // Fetch watchlist.json
    fetch("/collector/watchlist.json")
      .then((res) => res.json())
      .then((data) => setWatchlist(data))
      .catch(() => console.error("watchlist.json not found"));

    // Fetch daily_stock_data.json
    fetch("/collector/daily_stock_data.json")
      .then((res) => res.json())
      .then((data) => setStockData(data))
      .catch(() => console.error("daily_stock_data.json not found"));
  }, []);

  return (
    <table>
      <thead>
        <tr>
          <th>Symbol</th>
          <th>Name</th>
          <th>Price</th>
          <th>Change</th>
        </tr>
      </thead>
      <tbody>
        {watchlist.map((symbol) => {
          const stock = stockData[symbol] || {};
          return (
            <tr key={symbol}>
              <td>{symbol}</td>
              <td>{stock.name || "-"}</td>
              <td>{stock.price || "-"}</td>
              <td>{stock.change || "-"}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}

export default StockTable;
