import React, { useEffect, useState } from "react";

export default function StockTable() {
  const [watchlist, setWatchlist] = useState([]);
  const [stockData, setStockData] = useState({});

  useEffect(() => {
    // Fetch watchlist
    fetch("/collector/watchlist.json")
      .then((res) => res.json())
      .then((data) => setWatchlist(data))
      .catch((err) => console.error("Error loading watchlist:", err));

    // Fetch daily stock data
    fetch("/collector/daily_stock_data.json")
      .then((res) => res.json())
      .then((data) => setStockData(data))
      .catch((err) => console.error("Error loading stock data:", err));
  }, []);

  return (
    <div>
      <h2>Stock Watchlist</h2>
      <table>
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Price</th>
            <th>Change</th>
          </tr>
        </thead>
        <tbody>
          {watchlist.map((symbol) => (
            <tr key={symbol}>
              <td>{symbol}</td>
              <td>{stockData[symbol]?.price ?? "N/A"}</td>
              <td>{stockData[symbol]?.change ?? "N/A"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
