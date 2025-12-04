import React, { useEffect, useState } from "react";

const BASE_URL = "https://<username>.github.io/<repo-name>/datafiles/"; 
// Replace <username> and <repo-name> with your GitHub username and repo

export default function StockTable() {
  const [watchlist, setWatchlist] = useState([]);
  const [stockData, setStockData] = useState([]);

  useEffect(() => {
    // Fetch watchlist.json
    fetch(BASE_URL + "watchlist.json", { cache: "no-cache" })
      .then((res) => res.json())
      .then((data) => setWatchlist(data))
      .catch((err) => console.error("Error fetching watchlist:", err));

    // Fetch daily_stock_data.json
    fetch(BASE_URL + "daily_stock_data.json", { cache: "no-cache" })
      .then((res) => res.json())
      .then((data) => setStockData(data))
      .catch((err) => console.error("Error fetching stock data:", err));
  }, []);

  // Merge watchlist with stock data for display
  const displayData = watchlist.map((symbol) => {
    const stock = stockData.find((s) => s.symbol === symbol);
    return stock || { symbol, name: "-", price: "-", change: "-" };
  });

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
        {displayData.map((stock) => (
          <tr key={stock.symbol}>
            <td>{stock.symbol}</td>
            <td>{stock.name}</td>
            <td>{stock.price}</td>
            <td>{stock.change}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
